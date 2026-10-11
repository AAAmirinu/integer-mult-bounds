#include <bits/stdc++.h>
#include "json.hpp"
using namespace std;using J=nlohmann::json;
using Frame=bitset<512>;
Frame space(J a){Frame f;f[0]=1;for(auto z:a){int v=z;Frame g=f;for(int i=0;i<512;i++)if(f[i])g[i^v]=1;f=g;}return f;}
bool subset(Frame a,Frame b){return (a&~b).none();}
int main(int argc,char**argv){ifstream in(argv[1]);J w;in>>w;vector<J> ev;for(auto e:w["A"])ev.push_back(e);for(auto e:w["cut"])ev.push_back(e);for(auto e:w["B"])ev.push_back(e);
const int N=800,V=120;vector<array<double,120>> rows(N);vector<unsigned long long> hash(N);for(int i=0;i<V;i++)rows[i][i]=1;
auto rehash=[&](int r){unsigned long long h=1469598103934665603ull;for(double v:rows[r]){if(v==0)v=0;unsigned long long z;memcpy(&z,&v,8);h=(h^z)*1099511628211ull;}hash[r]=h;};for(int i=0;i<N;i++)rehash(i);
vector<bitset<800>> cand(N);vector<int> reads(N);for(int r=240;r<N;r++){cand[r].set();for(int t=120;t<240;t++)cand[r][t]=0;cand[r][r]=0;}
for(auto e:ev){string op=e[0];int r=e[1];if(op=="add"){int s=e[2];if(s>=240){reads[s]++;for(int t=0;t<N;t++)if(cand[s][t]&&(hash[t]!=hash[s]||rows[t]!=rows[s]))cand[s][t]=0;}double q=double(e[3].get<int>())/e[4].get<int>();for(int i=0;i<V;i++)rows[r][i]+=q*rows[s][i];}
else {double q=double(e[2].get<int>())/e[3].get<int>();for(double&x:rows[r])x*=q;}rehash(r);}
 J out=J::array();set<int> centres;for(auto x:w["centers"])centres.insert(x.get<int>());
vector<Frame> frames;for(auto e:ev)frames.push_back(space(e.back()));
for(int r=240;r<N;r++)if(reads[r]&&!centres.count(r))for(int t=0;t<N;t++)if(cand[r][t]){
 Frame f;f[0]=1;if(t<120)f=space(J::array({w["ports"][t]}));bool ok=true;int crossings=0;
 for(int k=0;k<(int)ev.size();k++){auto e=ev[k];int dst=e[1];if(dst==r)continue;string op=e[0];int src=op=="add"?e[2].get<int>():-1;if(dst==t||src==t||src==r){if(!subset(f,frames[k])){ok=false;break;}f=frames[k];crossings++;if(src==r&&dst==t){ok=false;break;}}}
 out.push_back({{"drop",r},{"keep",t},{"frame_chain_legal",ok},{"touches",crossings}});
}
ofstream o(argv[2]);o<<out.dump(2)<<"\n";cout<<"same-value candidates "<<out.size()<<", compatible "<<count_if(out.begin(),out.end(),[](auto x){return x["frame_chain_legal"].template get<bool>();})<<"\n";
}
