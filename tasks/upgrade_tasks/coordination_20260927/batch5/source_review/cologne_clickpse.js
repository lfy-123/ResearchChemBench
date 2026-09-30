var format="molpro";
var language="de";
var anzBack = 0;
var befehl = "/cgi-bin/pp.pl?job=listecps";
function openOptions(width,height,scroll){
 if(!width) width=400;
 if(!height) height=400;
 if(!scroll) scroll=0;
 var left = parseInt(screen.availWidth/2)  - parseInt(width/2);
 var top  = parseInt(screen.availHeight/2) - parseInt(height/2);
 return " width="+width +",height="+height +",left="+left +",top="+top +",resizable=1" +",status=1" +",scrollbars="+scroll +",dependent=1";
}
function zeigElement(Element) {
 cmd = befehl + ",format=" + format + ",element=" + Element + ",language=" + language;
 fnstr = open(cmd, "ElemFenster", openOptions(800,700,1));
 fnstr.focus();
 //  window.location.replace(cmd);
} // function zeigElement(Element)
function shownav(navname, welches) {
 if (navname.length != 2) { navname = this.id; }
 hideall();
 showobject(navname);
}
function hidenav(navname) {
 if (navname.length != 2) { navname = this.id; }
 hideobject(navname);
}
function hideall() {
 hideobject('HL');
}
function hideobject(objname) {
 if (document.all) { //IE
  document.all[objname].style.visibility="hidden";
  eval('document.all.'+objname+'.style.visibility="hidden"');
 }
 if (document.layers) { //NS
  document.layers[objname].visibility="hide";
  eval('document.'+objname+'.document.visibility="hide"');
 }
 if (document.getElementById) {
  document.getElementById(objname).style.visibility="hidden";
 }
} // function hideobject(objname)
function showobject(objname) {
 if (document.all) {
  document.all[objname].style.visibility="visible";
  eval('document.all.'+objname+'.style.visibility="visible"');
 }
 if (document.layers) {
  document.layers[objname].visibility="show";
  eval('document.'+objname+'.document.visibility="show"');
 }
 if (document.getElementById) {
  document.getElementById(objname).style.visibility="visible";
 }
} // function showobject(objname)
