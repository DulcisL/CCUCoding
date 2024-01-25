using System;

// Properties with backing fields & get/set
public class Person
{
    private string _name;
    private string _id;

    public string? Name
    {
        get
        {
            return _name;
        }
    }

    public string? Id
    {
        get
        {
            return _id;
        }
        set
        {
            if (value != null && value.Length != 9)
            {
                throw new ArgumentException("Not a valid ID");
            }
            _id = value;
        }
    }

    public Person(string name, string? id)
    {
        _name = name;
        Id = id;
    }
}

// Properties with backing fields & expression and body def.
public class Person2
{
    private string _first;
    private string _last;

    public string Name => $"{_first} {_last}";

    public Person2(string first, string last)
    {
        _first = first;
        _last = last;
    }
}

// Auto-implemented
public class Person3
{
    public string First { get; set; }
    public string Last { get; set; }

    public Person3() { } // Add default constructor

    public Person3(string first, string last)
    {
        First = first;
        Last = last;
    }
}

class Program
{
    static void Main()
    {
        var person1 = new Person("Jeff", "123456789");
        Console.WriteLine($"Look at {person1.Name}");

        var person2 = new Person2("John", "Doe");
        Console.WriteLine($"Say hello to {person2.Name}");

        var person3 = new Person3 { First = "Jeff", Last = "Dom" };
        Console.WriteLine($"Meet {person3.First} {person3.Last}");

        Console.ReadLine();
    }
}
