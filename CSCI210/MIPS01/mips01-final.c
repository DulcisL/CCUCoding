#include <stdio.h>

void swap(int v[], int k);
void sort(int v[], int n);
void print_array(int v[], int n);
void sort_descending(int v[], int n);

int main(void) {
  int A[] = {2, 4, 3, 1, 9, 7}; //.data .word A[2,4,3,1,9,7]
  int N = 6;                    // Length of A

  print_array(A, N);
  sort(A, N);
  print_array(A, N);
  sort_descending(A, N);
  print_array(A, N);

  return 0;
}

void swap(int v[], int k) {
  int temp = v[k];
  v[k] = v[k + 1];
  v[k + 1] = temp;
}

void sort(int v[], int n) {
  for (int i = 0; i < n; i++) {
    for (int j = i - 1; j >= 0; j--) {
      if (v[j + 1] < v[j])
        swap(v, j);
      else
        break;
    }
  }
}

void sort_descending(int v[], int n) {
  for (int i = 0; i < n; i++) {
    for (int j = i - 1; j >= 0; j--) {
      if (v[j + 1] > v[j]) { // Compare for descending order
        swap(v, j);
      } else {
        break;
      }
    }
  }
}

void print_array(int v[], int n) {
  for (int i = 0; i < n; i++) {
    printf("%d ", v[i]);
  }
  printf("\n");
}
