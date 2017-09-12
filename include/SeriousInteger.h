#ifndef SERIOUSINTEGER_H
#define SERIOUSINTEGER_H

#include <boost/multiprecision/cpp_int.hpp>
#include "SeriousFwd.h"

class SeriousInteger {
public:
    typedef boost::multiprecision::cpp_int Integer;
    SeriousInteger();
    virtual ~SeriousInteger();
    Integer value() const;

protected:

private:
    Integer _value;
};

#endif // SERIOUSINTEGER_H
