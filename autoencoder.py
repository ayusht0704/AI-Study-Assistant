1. Insertion sort
#include <stdio.h>
int main() {
 int a[] = {4, 5, 2, 3};
 int n = 4, i, j, key;
 for(i = 1; i < n; i++) {
 key = a[i];
 j = i - 1;
 while(j >= 0 && a[j] > key) {
 a[j+1] = a[j];
 j--;
 }
 a[j+1] = key;
 }
 printf("Sorted array: ");
 for(i = 0; i < n; i++)
 printf("%d ", a[i]);
 return 0;
}
2. Binary Search + Min Max
#include <stdio.h>
int main() {
 int a[] = {2, 4, 5, 7, 9};
 int n = 5, x = 7;
 int l = 0, r = n - 1, mid;
 // Binary Search
 while(l <= r) {
 mid = (l + r) / 2;
 if(a[mid] == x) {
 printf("Found at index: %d\n", mid);
 break;
 }
 else if(a[mid] < x)
 l = mid + 1;
 else
 r = mid - 1;
 }
 // Min Max
 int min = a[0], max = a[0];
 for(int i = 0; i < n; i++) {
 if(a[i] < min) min = a[i];
 if(a[i] > max) max = a[i];
 }
 printf("Min: %d Max: %d", min, max);
 return 0;
}
3. Merge Sort
#include <stdio.h>
void merge(int a[], int l, int m, int r) {
 int i = l, j = m+1, k = 0, temp[100];
 while(i <= m && j <= r) {
 if(a[i] < a[j]) temp[k++] = a[i++];
 else temp[k++] = a[j++];
 }
 while(i <= m) temp[k++] = a[i++];
 while(j <= r) temp[k++] = a[j++];
 for(i = l, k = 0; i <= r; i++, k++)
 a[i] = temp[k];
}
void mergeSort(int a[], int l, int r) {
 if(l < r) {
 int m = (l + r) / 2;
 mergeSort(a, l, m);
 mergeSort(a, m+1, r);
 merge(a, l, m, r);
 }
}
int main() {
 int a[] = {5, 2, 9, 1, 7};
 int n = 5;
 mergeSort(a, 0, n-1);
 printf("Sorted: ");
 for(int i = 0; i < n; i++)
 printf("%d ", a[i]);
 return 0;
}
5. Knapsack (Greedy / Fractional)
#include <stdio.h>
int main() {
 int profit[] = {60, 100, 120};
 int weight[] = {10, 20, 30};
 int n = 3, capacity = 50;
 float ratio[3], total = 0;
 for(int i = 0; i < n; i++)
 ratio[i] = (float)profit[i] / weight[i];
 for(int i = 0; i < n-1; i++) {
 for(int j = i+1; j < n; j++) {
 if(ratio[i] < ratio[j]) {
 float t = ratio[i]; ratio[i] = ratio[j]; ratio[j] = t;
 int tp = profit[i]; profit[i] = profit[j]; profit[j] = tp;
 int tw = weight[i]; weight[i] = weight[j]; weight[j] = tw;
 }
 }
 }
 for(int i = 0; i < n; i++) {
 if(capacity >= weight[i]) {
 capacity -= weight[i];
 total += profit[i];
 } else {
 total += profit[i] * ((float)capacity / weight[i]);
 break;
 }
 }
 printf("Max Profit: %.2f", total);
 return 0;
}
4. Quick sort
#include <stdio.h>
void qs(int a[], int l, int r){
 int i=l, j=r, p=a[l], t;
 while(i<j){
 while(a[i]<=p && i<r) i++;
 while(a[j]>p) j--;
 if(i<j){ t=a[i]; a[i]=a[j]; a[j]=t; }
 }
 t=a[l]; a[l]=a[j]; a[j]=t;
 qs(a,l,j-1);
 qs(a,j+1,r);
}
int main(){
 int a[]={5,2,9,1,7}, n=5;
 qs(a,0,n-1);
 for(int i=0;i<n;i++) printf("%d ",a[i]);
}