%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear
clc
format short G
d=load(N2.txt'); % columns are T, St, and H_vap
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
d_bond=1.4119; %bond length from NIST database
tc=144; % critical temperature from NIST database
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
t=d(:,1);
st=d(:,2);
gama0=((1-t./tc).^(11/9))\st;
hv=d(:,3);
S_TE=(0.5*gama0*(2*(1-t/tc).^(11/9)+11/9*t.*(1t/tc).^(2/9)./tc))\(hv+8.314/2.*t.*log(t/tc));
S_TE=S_TE/6.022e23*1e20;
out=NaN(8005,2);
ii=1;
for r_atom=1.3:0.0001:2.1
r1=r_atom;
r2=r_atom;
cos_alpha1=(r2^2-r1^2-d_bond^2)/(-2*r1*d_bond);
cos_alpha2=(r1^2-r2^2-d_bond^2)/(-2*r2*d_bond);
s_vdw=4*pi*(r1^2+r2^2)-2*pi*r1^2*(1-cos_alpha1)-2*pi*r2^2*(1-cos_alpha2);
4
out(ii,1)=r_atom;
out(ii,2)=abs(s_vdw-S_TE);
ii=ii+1;
end
out=out(1:ii-1,:);
f=find(out(:,2)==min(out(:,2)));
out(f,:);
r_element=out(f,1)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%