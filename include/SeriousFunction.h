#ifndef SERIOUSFUNCTION_H_INCLUDED
#define SERIOUSFUNCTION_H_INCLUDED

#include "SeriousFwd.h"
#include <functional>

class SeriousFunction {
public:
    typedef std::function<const SeriousStack(const SeriousStack)> serious_function_type;
    SeriousFunction(serious_function_type fn): _fn(fn) {}

    const serious_function_type fn() const;

protected:

private:
    const serious_function_type _fn;
};

#endif // SERIOUSFUNCTION_H_INCLUDED