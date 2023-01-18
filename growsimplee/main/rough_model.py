"""import pandas as pd

dataframe1 = pd.read_excel('bangalore_pickups.xlsx')
dataframe2 = pd.read_excel('bangalore_dispatch_address_finals.xlsx')

# print(dataframe1)
# print(dataframe2)


# from collections import defaultdict
  
# # function for adding edge to graph
# graph = defaultdict(list)
# def addEdge(graph,u,v):
#     graph[u].append(v)
  
# # definition of function
# def generate_edges(graph):
#     edges = []
  
#     # for each node in graph
#     for node in graph:
          
#         # for each neighbour node of a single node
#         for neighbour in graph[node]:
              
#             # if edge exists then append
#             edges.append((node, neighbour))
#     return edges



#     # declaration of graph as dictionary
# addEdge(graph,'a','c')
# addEdge(graph,'b','c')
# addEdge(graph,'b','e')
# addEdge(graph,'c','d')
# addEdge(graph,'c','e')
# addEdge(graph,'c','a')
# addEdge(graph,'c','b')
# addEdge(graph,'e','b')
# addEdge(graph,'d','c')
# addEdge(graph,'e','c')
  
# # Driver Function call 
# # to print generated graph
# print(generate_edges(graph)) 






# import copy
# import random



# no_of_delivery_man = 5
# delivery_man_addr = [0, 0]

# delivery_addr = [[2, 2], [1, 5], [1, 7], [2, 9], [5, 6], [3, 7], [2, 9], [4, 8]]


# delivery_man_delivery_locations = []
# for _ in range(no_of_delivery_man):
#     delivery_man_delivery_locations.append([])
# print(delivery_man_delivery_locations[4])


# iterations = 5

# while iterations > 0:
#     iterations -= 1
#     temp_del_addr = copy.deepcopy(delivery_addr)
#     random.shuffle(temp_del_addr)
#     #print(temp_del_addr)
#     total_addrs = len(temp_del_addr)
#     delivery_man_delivery_locations.clear()
#     for _ in range(no_of_delivery_man):
#         delivery_man_delivery_locations.append([])
#     for i in range(0 ,min(no_of_delivery_man ,total_addrs)):
#         delivery_man_delivery_locations[i].append(temp_del_addr[i])

    


#     print(delivery_man_delivery_locations)



# no_of_delivery_man = 5
# delivery_man_addr = [0, 0]

# delivery_addr = [[2, 2], [1, 5], [1, 7], [2, 9], [5, 6], [3, 7], [2, 9], [4, 8]]


# delivery_man_delivery_locations = []



import random
import sys



def ReadData(filename):

	# Read the file, splitting by lines
	f = open(filename, 'r');
	lines = f.read().splitlines();
	f.close();

	items = [];

	for i in range(1, len(lines)):
		line = lines[i].split(',');
		itemFeatures = [];

		for j in range(len(line)-1):
			
			# Convert feature value to float
			v = float(line[j]);
			
			# Add feature value to dict
			itemFeatures.append(v);

		items.append(itemFeatures);

	random.shuffle(items);

	return items;

# print(ReadData('data.txt'))



def FindColMinMax(items):
	n = len(items[0]);
	minima = [sys.maxint for i in range(n)]
	maxima = [-sys.maxint -1 for i in range(n)]
	
	for item in items:
		for f in range(len(item)):
			if (item[f] < minima[f]):
				minima[f] = item[f]
			
			if (item[f] > maxima[f]):
				maxima[f] = item[f]    
    return 0



def InitializeMeans(items, k, cMin, cMax):
    
	# Initialize means to random numbers between
	# the min and max of each column/feature	
	f = len(items[0]); # number of features
	means = [[0 for i in range(f)] for j in range(k)];
	
	for mean in means:
		for i in range(len(mean)):

			# Set value to a random float
			# (adding +-1 to avoid a wide placement of a mean)
			mean[i] = uniform(cMin[i]+1, cMax[i]-1);

	return means;


def EuclideanDistance(x, y):
    	S = 0; # The sum of the squared differences of the elements
	for i in range(len(x)):
		S += math.pow(x[i]-y[i], 2)

	#The square root of the sum
	return math.sqrt(S)



def UpdateMean(n,mean,item):
    	for i in range(len(mean)):
		m = mean[i];
		m = (m*(n-1)+item[i])/float(n);
		mean[i] = round(m, 3);
	
	return mean;



def Classify(means,item):
    
	# Classify item to the mean with minimum distance	
	minimum = sys.maxint;
	index = -1;

	for i in range(len(means)):

		# Find distance from item to mean
		dis = EuclideanDistance(item, means[i]);

		if (dis < minimum):
			minimum = dis;
			index = i;
	
	return index;


def CalculateMeans(k,items,maxIterations=100000):
    
	# Find the minima and maxima for columns
	cMin, cMax = FindColMinMax(items);
	
	# Initialize means at random points
	means = InitializeMeans(items,k,cMin,cMax);
	
	# Initialize clusters, the array to hold
	# the number of items in a class
	clusterSizes= [0 for i in range(len(means))];

	# An array to hold the cluster an item is in
	belongsTo = [0 for i in range(len(items))];

	# Calculate means
	for e in range(maxIterations):

		# If no change of cluster occurs, halt
		noChange = True;
		for i in range(len(items)):

			item = items[i];

			# Classify item into a cluster and update the
			# corresponding means.		
			index = Classify(means,item);

			clusterSizes[index] += 1;
			cSize = clusterSizes[index];
			means[index] = UpdateMean(cSize,means[index],item);

			# Item changed cluster
			if(index != belongsTo[i]):
				noChange = False;

			belongsTo[i] = index;

		# Nothing changed, return
		if (noChange):
			break;

	return means;



def FindClusters(means,items):
    	clusters = [[] for i in range(len(means))]; # Init clusters
	
	for item in items:

		# Classify item into a cluster
		index = Classify(means,item);

		# Add item to cluster
		clusters[index].append(item);

	return clusters;













from collections import defaultdict

def find_mst(graph, constraints):
    n = len(graph) # number of nodes in the graph
    mst = [] # list to store the edges of the MST
    visited = [False] * n # list to keep track of visited nodes
    while True:
        # Find the cheapest edge that connects each connected component to a new vertex
        cheapest_edges = defaultdict(list)
        for i in range(n):
            for j in range(i+1, n):
                if visited[i] == visited[j]:
                    continue
                if (i, j) not in constraints and (j, i) not in constraints:
                    continue
                weight = graph[i][j]
                if visited[i]:
                    cheapest_edges[j].append((i, j, weight))
                else:
                    cheapest_edges[i].append((i, j, weight))
        
        # Add the cheapest edges to the MST
        new_visited = [False] * n
        for edges in cheapest_edges.values():
            edges.sort(key=lambda x: x[2])
            mst.append(edges[0])
            new_visited[edges[0][0]] = True
            new_visited[edges[0][1]] = True
        
        # Check if all nodes have been visited
        if all(visited):
            break
        visited = new_visited
    
    return mst

# Example usage
graph = [[0, 2, 4, 0, 0],
         [2, 0, 2, 4, 2],
         [4, 2, 0, 0, 3],
         [0, 4, 0, 0, 3],
         [0, 2, 3, 3, 0]]

constraints = [(0, 1), (1, 2), (2, 4)]

print(find_mst(graph, constraints))






"""




# from collections import defaultdict

# def findMSDT(n, edges, queries):
#     # Sort edges by weight
#     edges = sorted(edges, key=lambda x: x[2])
#     # Create a dictionary to store visited nodes
#     visited = defaultdict(int)
#     # Initialize the result tree as an empty list
#     tree = []
#     # Initialize the number of edges in the tree to 0
#     num_edges = 0
#     # Iterate over edges
#     for edge in edges:
#         a, b, w = edge
#         # Check if adding the edge would create a cycle
#         if visited[a] < visited[b]:
#             # Check if adding the edge would violate the constraints of the query
#             if (a, b) not in queries:
#                 # If not, add the edge to the tree
#                 tree.append(edge)
#                 num_edges += 1
#                 visited[b] = max(visited[b], visited[a] + 1)
#         # If the tree has n-1 edges, it is a spanning tree
#         if num_edges == n-1:
#             break
#     return tree

# # Example usage:
# n = 4 
# edges = [(0, 1, 2), (0, 2, 3), (1, 2, 4), (1, 3, 5), (2, 3, 6)]
# queries = [(0, 1), (1, 2)]
# print(findMSDT(n, edges, queries))
# # Output: [(0, 1, 2), (1, 2, 4)]


'''

C++ code for ordering items in bag
 
 
 
#include<bits/stdc++.h>
#include<ext/pb_ds/assoc_container.hpp>
#include<ext/pb_ds/tree_policy.hpp>
 
using namespace std;
using namespace __gnu_pbds;
 
#define fastio() ios_base::sync_with_stdio(false);cin.tie(NULL);cout.tie(NULL)
#define flash ios_base::sync_with_stdio(0);cin.tie(0);
#define MOD 1000000007
#define MOD1 998244353
#define INF (ll)2e18
#define nline "\n"
#define pb push_back
#define ppb pop_back
#define ff first
#define ss second
#define PI 3.141592653589793238462
#define set_bits __builtin_popcountll
#define sz(x) ((ll)(x).size())
#define all(x) (x).begin(), (x).end()
#define srt(x) sort(x.begin(),x.end())
 
 
typedef long long ll;
typedef unsigned long long ull;
typedef long double lld;
//typedef tree<ll, null_type, less<ll>, rb_tree_tag, tree_order_statistics_node_update > pbds; // find_by_order, order_of_key
typedef tree<pair<ll, ll>, null_type, less<pair<ll, ll>>, rb_tree_tag, tree_order_statistics_node_update > pbds; // find_by_order, order_of_key
 
 
 
#ifndef ONLINE_JUDGE
#define debug(x) cerr << #x <<" "; _print(x); cerr << endl;
#else
#define debug(x)
#endif
 
void _print(ll t) {cerr << t;}
void _print(int t) {cerr << t;}
void _print(string t) {cerr << t;}
void _print(char t) {cerr << t;}
void _print(lld t) {cerr << t;}
void _print(double t) {cerr << t;}
void _print(ull t) {cerr << t;}
 
template <class T, class V> void _print(pair <T, V> p);
template <class T> void _print(vector <T> v);
template <class T> void _print(set <T> v);
template <class T, class V> void _print(map <T, V> v);
template <class T> void _print(multiset <T> v);
template <class T, class V> void _print(pair <T, V> p) {cerr << "{"; _print(p.ff); cerr << ","; _print(p.ss); cerr << "}";}
template <class T> void _print(vector <T> v) {cerr << "[ "; for (T i : v) {_print(i); cerr << " ";} cerr << "]";}
template <class T> void _print(set <T> v) {cerr << "[ "; for (T i : v) {_print(i); cerr << " ";} cerr << "]";}
template <class T> void _print(multiset <T> v) {cerr << "[ "; for (T i : v) {_print(i); cerr << " ";} cerr << "]";}
template <class T, class V> void _print(map <T, V> v) {cerr << "[ "; for (auto i : v) {_print(i); cerr << " ";} cerr << "]";}


ll power(ll a, ll b){ll ans=1; while(b){if(b&1)ans = (ans*a)%MOD;a = (a*a)%MOD;b>>=1;} return ans;}
ll power1(ll a, ll b){ll ans=1; while(b){if(b&1)ans = (ans*a);a = (a*a);b>>=1;} return ans;}
ll phin(ll n) {ll number = n; if (n % 2 == 0) {number /= 2; while (n % 2 == 0)n /= 2;} for (ll i = 3; i <= sqrt(n); i += 2) {if (n % i == 0) {while (n % i == 0)n /= i; number = (number / i * (i - 1));}} if (n > 1)number = (number / n * (n - 1)) ; return number;} //O(sqrt(N))
ll expo(ll a, ll b, ll mod) {ll res = 1; while (b > 0) {if (b & 1)res = (res * a) % mod; a = (a * a) % mod; b = b >> 1;} return res;}
ll mminvprime(ll a, ll b) {return expo(a, b - 2, b);}
ll mod_add(ll a, ll b, ll m) {a = a % m; b = b % m; return (((a + b) % m) + m) % m;}
ll mod_mul(ll a, ll b, ll m) {a = a % m; b = b % m; return (((a * b) % m) + m) % m;}
ll mod_sub(ll a, ll b, ll m) {a = a % m; b = b % m; return (((a - b) % m) + m) % m;}
ll mod_div(ll a, ll b, ll m) {a = a % m; b = b % m; return (mod_mul(a, mminvprime(b, m), m) + m) % m;}  //only for prime m
ll dx[] = {1,0,-1,0,1,-1,1,-1};
ll dy[] = {0,1,0,-1,1,1,-1,-1};
// bool isvalid(ll x, ll y){if(x>=1 && x <= n && y >= 1 && y <= m && mat[x][y] != '#' && vis[x][y] == 0){return true;}return false;}
// string ds = "RLDU";
// vector<vector<ll>> adj, adj2;
// map<pair<ll,ll>,ll>  dp;
// vector<ll> vis;



ll helper(ll ind, vector<ll> &v, ll b, vector<ll> st1, vector<ll> st2){

    debug(st1)debug(st2)

    if(ind >= v.size()){
        return 0LL;
    }

    ll max1 = 0, max2 = 0, cnt = 0;

    if(v[ind] > 0){
        st1.push_back(v[ind]);
    }else{
        if(!st1.empty() && st1.back() == -v[ind]){
            cnt++;
            st1.pop_back();
        }
        if(!st2.empty() && st2.back() == -v[ind]){
            cnt++;
            st2.pop_back();
        }
        auto it = st1.begin();
        for(ll i = 0; i < st1.size(); i++){
            if(st1[i] == -v[ind]){
                st1.erase(it);
                break;
            }
            it++;
        }
        auto it2 = st2.begin();
        for(ll i = 0; i < st2.size(); i++){
            if(st2[i] == -v[ind]){
                st2.erase(it2);
                break;
            }
            it2++;
        }
    }

    max1 = helper(ind + 1, v, 0LL, st1, st2);

    if(v[ind] > 0){
        st1.pop_back();
        st2.push_back(v[ind]);
    }

    max2 = helper(ind + 1, v, 1LL, st1, st2);

    return max(max1, max2) + cnt;

}



 
void solve(){
 
    ll TC = 1;
    // cin >> TC;
 
 
 
    while(TC--){


            ll n = 12;
            vector<ll> v = {1, 3, 2, 4, 6, 5, -2, -4, -6, -1, -5, -3}, st1, st2;

            // ll n = 6;
            // vector<ll> v = {1, 2, 3, -1, -3, -2}, st1, st2;




            ll ans = helper(0, v, 0, st1, st2);
            ans = max(ans, helper(0, v, 1, st1, st2));

            debug(ans)


        
        
            
            }
 
 
}
 
 
 
 

 
 
int main() {
#ifndef ONLINE_JUDGE
    freopen("Error.txt", "w", stderr);
#endif
 
     flash
    solve();
  //  cout<<fixed<<setprecision(10)<<mx<<"\n";
  //  divide by 2.0 to prevent precision errors
  
}

'''