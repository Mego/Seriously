#ifndef SERIOUSFLOAT_H
#define SERIOUSFLOAT_H

#include "SeriousFwd.h"

class SeriousFloat {
public:
    SeriousFloat();
    SeriousFloat(double value): _value(value) {}
    const double value() const;

protected:

private:
    const double _value;
};

#endif // SERIOUSFLOAT_H
