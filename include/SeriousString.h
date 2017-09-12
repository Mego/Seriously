#ifndef SERIOUSSTRING_H
#define SERIOUSSTRING_H

#include <string>
#include "SeriousFwd.h"

class SeriousString {
public:
    SeriousString();
    virtual ~SeriousString();
    std::string value() const;

protected:

private:
    std::string _value;
};

#endif // SERIOUSSTRING_H
