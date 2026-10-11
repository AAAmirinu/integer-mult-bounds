#include <iostream>
#include <vector>
#include <string>
using namespace std;
using U=unsigned long long; using W=__uint128_t;
const U P=(1ULL<<61)-1;
U mul(U a,U b){return (W)a*b%P;}
U power(U a,U n){U r=1;for(;n;n>>=1,a=mul(a,a))if(n&1)r=mul(r,a);return r;}
U parse(string s){bool neg=s[0]=='-';U r=0;for(int i=neg;i<(int)s.size();++i)r=((W)r*10+s[i]-'0')%P;return neg&&r?P-r:r;}
int main(){int n,cap;cin>>n>>cap;vector<vector<U>> a(cap,vector<U>(n));for(int i=0;i<n;++i)a[i][i]=1;
 string op;int positive=0,zero=0,index=0;vector<int> hits;
 while(cin>>op){++index;int t,s,rank;string x,y;
  if(op=="clear"){cin>>t;fill(a[t].begin(),a[t].end(),0);}
  else if(op=="copy"){cin>>t>>s;a[t]=a[s];}
  else if(op=="add"){cin>>t>>s>>x>>y;U q=mul(parse(x),power(parse(y),P-2));for(int i=0;i<n;++i)a[t][i]=(a[t][i]+mul(q,a[s][i]))%P;}
  else if(op=="scale"){cin>>t>>x>>y;U q=mul(parse(x),power(parse(y),P-2));for(auto &v:a[t])v=mul(v,q);}
  else if(op=="child"){cin>>t>>rank;++positive;bool allzero=true;for(auto v:a[t])allzero&=v==0;if(allzero){++zero;hits.push_back(index);}}
  else return 2;
 }
 cout<<"{\"positive_recursive_sites\":"<<positive<<",\"zero_candidates\":"<<zero<<",\"candidate_event_ids\":[";for(int i=0;i<(int)hits.size();++i)cout<<(i?",":"")<<hits[i];cout<<"],\"modulus\":\"2305843009213693951\",\"scope\":\"A nonzero modular entry disproves exact zero; any zero candidate needs independent rational replay.\"}\n";
}
