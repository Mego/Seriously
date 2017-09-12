#ifndef SERIOUSFLOAT_H
#define SERIOUSFLOAT_H

#include "SeriousFwd.h"

class SeriousFloat {
public:
    SeriousFloat();
    virtual ~SeriousFloat();
    double value() const;

protected:

private:
    double _value;
};

#endif // SERIOUSFLOAT_H
