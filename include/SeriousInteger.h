#ifndef SERIOUSINTEGER_H
#define SERIOUSINTEGER_H

#include <utility>
#include <boost/multiprecision/cpp_int.hpp>
#include "SeriousFwd.h"

class SeriousInteger {
public:
    typedef boost::multiprecision::cpp_int Integer;
    SeriousInteger(long long value): _value(value) {}
    const Integer value() const;

protected:

private:
    const Integer _value;
};

#endif // SERIOUSINTEGER_H
