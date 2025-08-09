#include <bits/stdc++.h>
using namespace std;

int partitionVec(vector<int>& a, int l, int r) {
    int pivot = a[r];
    int i = l;
    for (int j = l; j < r; ++j) {
        if (a[j] <= pivot) {
            swap(a[i], a[j]);
            ++i;
        }
    }
    swap(a[i], a[r]);
    return i;
}

void quickSort(vector<int>& a, int l, int r) {
    if (l >= r) return;
    int p = partitionVec(a, l, r);
    quickSort(a, l, p - 1);
    quickSort(a, p + 1, r);
}
int main() {
    int len;
    cin >> len;
    vector<int> arr(len);
    for (int i = 0; i < len; i++) cin >> arr[i];

    if (len > 0) quickSort(arr, 0, len - 1);
    for (int i = 0; i < len; ++i) {
        if (i) cout << ' ';
        cout << arr[i];
    }
    if (len) cout << '\n';
    
    return 0;
}