#ifndef SERIOUSLIST_H
#define SERIOUSLIST_H

#include <vector>
#include <initializer_list>
#include "SeriousFwd.h"

class SeriousList {
public:
    typedef std::vector<SeriousObject> List;
    SeriousList(std::initializer_list<SeriousObject> l): _value(l) {}
    const List value() const;

protected:

private:
    const List _value;
};

#endif // SERIOUSLIST_H
