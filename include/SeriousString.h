#ifndef SERIOUSSTRING_H
#define SERIOUSSTRING_H

#include <string>
#include "SeriousFwd.h"

class SeriousString {
public:
    SeriousString(): _value("") {}
    SeriousString(const std::string str): _value(str) {}
    SeriousString(const char* str): _value(str) {}
    const std::string value() const;

protected:

private:
    std::string _value;
};

#endif // SERIOUSSTRING_H
