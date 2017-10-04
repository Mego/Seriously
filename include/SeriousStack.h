#ifndef SERIOUSSTACK_H_INCLUDED
#define SERIOUSSTACK_H_INCLUDED

#include "SeriousFwd.h"
#include "SeriousObject.h"
#include <stack>

class SeriousStack : public std::stack<SeriousObject> {

};

#endif // SERIOUSSTACK_H_INCLUDED