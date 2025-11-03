#include <stdio.h>
#include <string.h>

int main()
{
  // INFO: This is not the real solution, but feel free to use this template.
  char arr[100];
  memset(arr, 'l', sizeof arr);

  int idx;
  scanf("%d", &idx);
  printf("%c", arr[idx]);
}
