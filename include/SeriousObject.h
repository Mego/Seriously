#ifndef SERIOUSOBJECT_H_INCLUDED
#define SERIOUSOBJECT_H_INCLUDED

#include "SeriousFwd.h"
#include "SeriousInteger.h"
#include "SeriousFloat.h"
#include "SeriousFunction.h"
#include "SeriousString.h"
#include "SeriousList.h"
#include <boost/variant.hpp>

class SeriousObject {
public:
    SeriousObject() = delete;
    SeriousObject(const SeriousInteger obj): _obj(obj) {}
    SeriousObject(const SeriousFloat obj): _obj(obj) {}
    SeriousObject(const SeriousFunction obj): _obj(obj) {}
    SeriousObject(const SeriousString obj): _obj(obj) {}
    SeriousObject(const SeriousList obj): _obj(obj) {}

    template<typename T>
    const T apply_visitor(boost::static_visitor<T> visitor) const;

    const SeriousInteger int_value() const;
    const SeriousFloat float_value() const;
    const SeriousFunction fn_value() const;
    const SeriousString string_value() const;
    const SeriousList list_value() const;

protected:

private:
    const boost::variant<SeriousInteger, SeriousFloat, SeriousFunction, SeriousString, SeriousList> _obj;
};

#endif // SERIOUSOBJECT_H_INCLUDED