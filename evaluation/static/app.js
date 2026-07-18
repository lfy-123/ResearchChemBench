const taskSelect = document.querySelector('#taskSelect');
const agentSelect = document.querySelector('#agentSelect');
const startButton = document.querySelector('#startButton');
const stopButton = document.querySelector('#stopButton');
const scoreButton = document.querySelector('#scoreButton');
const statusLabel = document.querySelector('#status');
const taskInfo = document.querySelector('#taskInfo');
const agentStream = document.querySelector('#agentStream');
const toolStream = document.querySelector('#toolStream');
const fileTree = document.querySelector('#fileTree');
const fileContent = document.querySelector('#fileContent');
const runsTable = document.querySelector('#runsTable');
let currentRun = null;
let eventSource = null;

async function jsonFetch(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || response.statusText);
  return data;
}

async function loadConfig() {
  const [tasks, config] = await Promise.all([jsonFetch('/api/tasks'), jsonFetch('/api/config')]);
  taskSelect.innerHTML = '';
  for (const [category, ids] of Object.entries(tasks)) {
    const group = document.createElement('optgroup');
    group.label = category;
    ids.forEach(id => group.append(new Option(id, id)));
    taskSelect.append(group);
  }
  agentSelect.innerHTML = '';
  for (const [key, value] of Object.entries(config.presets)) {
    agentSelect.append(new Option(value.label, key));
  }
  await loadTask();
  await loadRuns();
}

async function loadTask() {
  if (!taskSelect.value) return;
  const info = await jsonFetch(`/api/tasks/${taskSelect.value}/info`);
  taskInfo.textContent = JSON.stringify(info, null, 2);
}

function appendStream(element, value) {
  let rendered = value;
  try { rendered = JSON.stringify(JSON.parse(value), null, 2); } catch (_) {}
  element.textContent += rendered + '\n';
  element.scrollTop = element.scrollHeight;
}

function connectStream(runId) {
  if (eventSource) eventSource.close();
  eventSource = new EventSource(`/api/runs/${runId}/stream`);
  eventSource.onmessage = async event => {
    const payload = JSON.parse(event.data);
    if (payload.stream === 'agent') appendStream(agentStream, payload.line);
    if (payload.stream === 'tool') appendStream(toolStream, payload.line);
    if (payload.stream === 'system') {
      statusLabel.textContent = payload.status;
      startButton.disabled = false;
      stopButton.disabled = true;
      scoreButton.disabled = payload.status !== 'completed';
      eventSource.close();
      await loadFiles(runId);
      await loadRuns();
    }
  };
}

async function startRun() {
  agentStream.textContent = '';
  toolStream.textContent = '';
  fileContent.textContent = '';
  const run = await jsonFetch('/api/runs', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({task_id: taskSelect.value, agent: agentSelect.value})
  });
  currentRun = run.run_id;
  statusLabel.textContent = `running: ${currentRun}`;
  startButton.disabled = true;
  stopButton.disabled = false;
  scoreButton.disabled = true;
  connectStream(currentRun);
}

async function stopRun() {
  if (!currentRun) return;
  await jsonFetch(`/api/runs/${currentRun}/stop`, {method: 'POST'});
  statusLabel.textContent = 'stopping';
}

async function scoreRun() {
  if (!currentRun) return;
  statusLabel.textContent = 'scoring';
  const score = await jsonFetch(`/api/runs/${currentRun}/score`, {method: 'POST'});
  fileContent.textContent = JSON.stringify(score, null, 2);
  statusLabel.textContent = `score: ${score.score}`;
  await loadFiles(currentRun);
}

async function loadFiles(runId) {
  const files = await jsonFetch(`/api/runs/${runId}/files`);
  fileTree.innerHTML = '';
  files.forEach(item => {
    const element = document.createElement(item.type === 'file' ? 'button' : 'div');
    element.className = item.type;
    element.textContent = item.type === 'directory' ? `📁 ${item.path}` : `📄 ${item.path}`;
    if (item.type === 'file') element.onclick = () => loadFile(runId, item.path);
    fileTree.append(element);
  });
}

async function loadFile(runId, path) {
  const response = await fetch(`/api/runs/${runId}/file?path=${encodeURIComponent(path)}`);
  const type = response.headers.get('content-type') || '';
  fileContent.textContent = type.startsWith('text/') || type.includes('json')
    ? await response.text()
    : `[Binary file: ${path}]`;
}

async function loadRuns() {
  const runs = await jsonFetch('/api/runs');
  runsTable.innerHTML = '';
  runs.slice(0, 50).forEach(run => {
    const row = document.createElement('tr');
    row.dataset.run = run.run_id;
    row.innerHTML = `<td>${run.run_id}</td><td>${run.task_id}</td><td>${run.agent_name}</td><td>${run.status}</td><td>${run.duration_seconds ?? ''}</td>`;
    row.onclick = async () => {
      currentRun = run.run_id;
      statusLabel.textContent = run.status;
      startButton.disabled = false;
      stopButton.disabled = run.status !== 'running';
      scoreButton.disabled = run.status !== 'completed';
      await loadFiles(currentRun);
      const [output, trace] = await Promise.all([
        jsonFetch(`/api/runs/${currentRun}/output`),
        jsonFetch(`/api/runs/${currentRun}/trace`)
      ]);
      agentStream.textContent = output.join('\n');
      toolStream.textContent = trace.map(item => JSON.stringify(item, null, 2)).join('\n');
    };
    runsTable.append(row);
  });
}

taskSelect.addEventListener('change', loadTask);
startButton.addEventListener('click', () => startRun().catch(error => statusLabel.textContent = error.message));
stopButton.addEventListener('click', () => stopRun().catch(error => statusLabel.textContent = error.message));
scoreButton.addEventListener('click', () => scoreRun().catch(error => statusLabel.textContent = error.message));
loadConfig().catch(error => statusLabel.textContent = error.message);
