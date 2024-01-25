using System;
using System.Collections.Generic;
using System.Text;

namespace C_Prog
{
    class Program
    {
        static void Main(string[] args)
        {
            //Main Function
            ComicBook book1 = new ComicBook() 
            {
                ItemId = 4065,
                Name = "Spiderman",
                Description = "A story about a boy who is bitten by a radioactive spider giving him superpowers",
                DailyRentalCost = 2,
                ReplacementCost = 20,
                QuantityAvailable = 100,
                NumSeries = 165,
                MembershipDiscount = .20,
            };
            ComicBook book2 = new ComicBook() 
            {
                ItemId = 4072,
                Name = "The Incredible Hulk",
                Description = "A man hit with gamma radiation turns into the Incredible Hulk",
                DailyRentalCost = 2,
                ReplacementCost = 15,
                QuantityAvailable = 250,
                NumSeries = 105,
                MembershipDiscount = .30,
            };
            ComicBook book3 = new ComicBook() 
            {
                ItemId = 4061,
                Name = "Iron Man",
                Description = "A story about a super intellegent man who is tired of the evil in the world",
                DailyRentalCost = 3,
                ReplacementCost = 25,
                QuantityAvailable = 30,
                NumSeries = 20,
                MembershipDiscount = .15,
            };
            ComicBook book4 = new ComicBook() 
            {
                ItemId = 5044,
                Name = "The Avengers",
                Description = "A team of superheros rids the galaxy of evil",
                DailyRentalCost = 4,
                ReplacementCost = 15,
                QuantityAvailable = 300,
                NumSeries = 200,
                MembershipDiscount = .20,
            };
            ComicBook book5 = new ComicBook() 
            {
                ItemId = 0504,
                Name = "Star Wars",
                Description = "A story in a Galaxy Far far away",
                DailyRentalCost = 1,
                ReplacementCost = 22,
                QuantityAvailable = 50,
                NumSeries = 50,
                MembershipDiscount = .25,
            };
            ComicBook book6 = new ComicBook() 
            {
                ItemId = 6025,
                Name = "Batman",
                Description = "An Orphan Fights crime after watching his parents die",
                DailyRentalCost = 1,
                ReplacementCost = 15,
                QuantityAvailable = 350,
                NumSeries = 150,
                MembershipDiscount = .2,
            };
            ComicBook book7 = new ComicBook() 
            {
                ItemId = 3052,
                Name = "Scott Pilgrim VS The World",
                Description = "A man fighting the 7 deadly exes",
                DailyRentalCost = 1,
                ReplacementCost = 10,
                QuantityAvailable = 20,
                NumSeries = 10,
                MembershipDiscount = .30,
            };

            //Before Sort
            Console.WriteLine("Unsorted");
            Console.WriteLine("");
            List<ComicBook> Books = new List<ComicBook>(){
                book1, book2, book3, book4, book5, book6, book7
            };
            foreach (ComicBook b in Books){
                Console.WriteLine(b);
                Console.WriteLine($"Costs: ${b.ReplacementCost} to replace");
                Console.WriteLine($"With membership discount costs ${b.DailyRentalCost - b.DailyRentalCost * b.MembershipDiscount}"); 
                Console.WriteLine("");
            }

            //After Sort by ItemId
            Console.WriteLine("---------");
            Console.WriteLine("Sorted by Item ID (Default)");
            Console.WriteLine("");
            Books.Sort();
            foreach (ComicBook b in Books){
                Console.WriteLine(b);
                Console.WriteLine($"Costs: ${b.ReplacementCost} to replace");
                Console.WriteLine($"With membership discount costs ${b.DailyRentalCost - b.DailyRentalCost * b.MembershipDiscount}");
                Console.WriteLine("");
            }
            
            //After Sort by Name
            Console.WriteLine("---------");
            Console.WriteLine("Sorted by Name");
            Console.WriteLine("");
            Books.Sort(new NameComparer());
            foreach (ComicBook b in Books){
                Console.WriteLine(b);
                Console.WriteLine($"Costs: ${b.ReplacementCost} to replace");
                Console.WriteLine($"With membership discount costs ${b.DailyRentalCost - b.DailyRentalCost * b.MembershipDiscount}");
                Console.WriteLine("");
            }


            //After Sort by DailyRentalCost
            Console.WriteLine("---------");
            Console.WriteLine("Sorted By Rental Cost");
            Console.WriteLine("");
            Books.Sort(new RentalCostComparer());
            foreach (ComicBook b in Books){
                Console.WriteLine(b);
                Console.WriteLine($"Costs: ${b.ReplacementCost} to replace");
                Console.WriteLine($"With membership discount costs ${b.DailyRentalCost - b.DailyRentalCost * b.MembershipDiscount}");
                Console.WriteLine("");
            }


            //After Sort by QuantityAvailable
            Console.WriteLine("---------");
            Console.WriteLine("Sorted by Quantity Available");
            Console.WriteLine("");
            Books.Sort(new QuantityComparer());
            foreach (ComicBook b in Books){
                Console.WriteLine(b);
                Console.WriteLine($"Costs: ${b.ReplacementCost} to replace");
                Console.WriteLine($"With membership discount costs ${b.DailyRentalCost - b.DailyRentalCost * b.MembershipDiscount}");
                Console.WriteLine("");
            }

            //After Sort by NumSeries
            Console.WriteLine("---------");
            Console.WriteLine("Sorted by Number in the series");
            Console.WriteLine("");
            Books.Sort(new NumSeriesComparer());
            foreach (ComicBook b in Books){
                Console.WriteLine(b);
                Console.WriteLine($"Costs: ${b.ReplacementCost} to replace");
                Console.WriteLine($"With membership discount costs ${b.DailyRentalCost - b.DailyRentalCost * b.MembershipDiscount}");
                Console.WriteLine("");
            }
        }
    }

    //Comic Book Class
    public class ComicBook : IComparable<ComicBook>
    {
        //Properties
        public int ItemId {get;set;}
        public string Name {get;set;}
        public string Description {get;set;}
        public int DailyRentalCost {get;set;}
        public int ReplacementCost {get;set;}
        public int QuantityAvailable {get;set;}
        public int NumSeries {get;set;}
        private double _membershipdiscount;
        public double MembershipDiscount 
        {
            get { return this._membershipdiscount;}
            set 
            {
                if (value < 0 || value >= 1)
                    throw new ArgumentOutOfRangeException("Discount must be less than 1 and greater than 0");
                this._membershipdiscount = value;
            }
        }
        public override string ToString() 
        {
            return $"({ItemId}) {Name}({NumSeries}), {Description}, costs daily: ${DailyRentalCost}, There are {QuantityAvailable} books in the store";
        }

        public int CompareTo(ComicBook otherComicBook)
        {
            return this.ItemId.CompareTo(otherComicBook.ItemId);
        }
    }
    
    //Comparers
    public class NameComparer : IComparer<ComicBook>
    {
        public int Compare(ComicBook x, ComicBook y)
        {
            return x.Name.CompareTo(y.Name);
        }
    }
    public class RentalCostComparer : IComparer<ComicBook>
    {
        public int Compare(ComicBook x, ComicBook y)
        {
            return x.DailyRentalCost - y.DailyRentalCost;
        }
    }
    public class QuantityComparer : IComparer<ComicBook>
    {
        public int Compare(ComicBook x, ComicBook y)
        {
            return x.QuantityAvailable - y.QuantityAvailable;
        }
    }
    public class NumSeriesComparer : IComparer<ComicBook>
    {
        public int Compare(ComicBook x, ComicBook y)
            {
                return x.NumSeries - y.NumSeries;
            }
    }
}
