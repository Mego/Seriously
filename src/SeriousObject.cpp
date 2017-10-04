#include "SeriousExceptions.h"
#include "SeriousObject.h"

template<typename T>
const T SeriousObject::apply_visitor(boost::static_visitor<T> visitor) const {
    return boost::apply_visitor(visitor, this->_obj);
}

const SeriousInteger SeriousObject::int_value() const {
    return boost::get<SeriousInteger>(this->_obj);
}

const SeriousFloat SeriousObject::float_value() const {
    return boost::get<SeriousFloat>(this->_obj);
}

const SeriousFunction SeriousObject::fn_value() const {
    return boost::get<SeriousFunction>(this->_obj);
}

const SeriousString SeriousObject::string_value() const {
    return boost::get<SeriousString>(this->_obj);
}

const SeriousList SeriousObject::list_value() const {
    return boost::get<SeriousList>(this->_obj);
}