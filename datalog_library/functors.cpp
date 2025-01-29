#include <cstdint>
#include <cstddef>
#include <regex.h>
extern "C" {

int32_t regex_match(const char* pattern, const char* string)
{
  regex_t comp_patt;
  int value;

  value = regcomp( &comp_patt, pattern, 0);

  if (value == 0) {
    // compilation successful
  } else {
    // compilation failed
    return 2;
  }

  value = regexec( &comp_patt, string, 0, NULL, 0 );

  if (value == 0) {
    return 1;
  } else if (value == REG_NOMATCH) {
    return 0;
  } else {
    // error
    return 2;
  }
}

}