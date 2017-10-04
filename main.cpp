#include <iostream>
#include "Seriously.h"

using namespace std;

int main() {
    SeriousObject obj("Hello, World!");
    cout << obj.string_value().value() << endl;
    return 0;
}
