#ifndef SERIOUSLIST_H
#define SERIOUSLIST_H

#include <vector>
#include "SeriousFwd.h"

class SeriousList {
public:
    typedef std::vector<SeriousObject> List;
    SeriousList();
    virtual ~SeriousList();
    List value() const;

protected:

private:
    List _value;
};

#endif // SERIOUSLIST_H
