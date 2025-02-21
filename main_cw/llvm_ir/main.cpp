#include <cstdio>
#include <cwchar>
#include <clocale>
#include <cstring>
#include <cstdlib>

// Declare runtime helper functions with `extern "C"` to avoid name mangling
extern "C" void PrintI(int val) { printf("%d", val); }
extern "C" void PrintL(long val) { printf("%ld", val); }
extern "C" void PrintD(double val) { printf("%lf", val); }
extern "C" void PrintF(float val) { printf("%f", val); }
extern "C" void PrintS(const wchar_t* val) { printf("%ls", val); }

extern "C" wchar_t* StringConcat(wchar_t* lhs, wchar_t* rhs) {
    size_t lhsLength = wcslen(lhs);
    size_t rhsLength = wcslen(rhs);
    lhs = (wchar_t*)realloc(lhs, (lhsLength + rhsLength + 1) * sizeof(wchar_t));
    return wcscat(lhs, rhs);
}

extern "C" wchar_t* StringCopy(const wchar_t* str) {
    size_t length = wcslen(str);
    wchar_t* result = (wchar_t*)calloc(length + 1, sizeof(wchar_t));
    wcsncpy(result, str, length);
    return result;
}

// Main function of BASIC program
extern "C" wchar_t* Main(wchar_t** argv, int len);

int main(int argc, char** argv) {
    setlocale(LC_ALL, "C.UTF-8");

    // Convert command line argument array from char* to wchar_t*
    wchar_t** args = (wchar_t**)calloc(argc, sizeof(wchar_t*));
    for (int i = 0; i < argc; i++) {
        size_t length = strlen(argv[i]);
        args[i] = (wchar_t*)calloc(length + 1, sizeof(wchar_t));
        for (size_t j = 0; j < length; j++) {
            args[i][j] = argv[i][j];
        }
    }

    Main(args, argc);

    // Free memory
    for (int i = 0; i < argc; i++) {
        free(args[i]);
    }
    free(args);

    return 0;
}