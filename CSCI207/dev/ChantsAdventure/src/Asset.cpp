#include <Asset.hpp>

namespace chants
{
    Asset::Asset(string name, string message, int value, bool isOffensive)
    {
        _name = name;
        _message = message;
        _value = value;
        _isOffensive = isOffensive;
        hasBeenUsed = false;
    }

    string Asset::GetName()
    {
        return _name;
    }

    string Asset::GetMessage()
    {
        return _message;
    }

    int Asset::GetValue()
    {
        return _value;
    }

    bool Asset::isOffensive()
    {
        return _isOffensive;
    }

}