using System;
using System.Collections.Generic;

namespace TV
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");

            Show one = new Show() {
                Name="Parks and Recreation",
                NumEpisodes=125,
                Year=2009,
                Actors= new List<string> {
                    "Amy Poehler","Aziz Ansari","Nick Offerman"
                }
            };
            Show two = new Show() {
                Name="Burn Notice",
                NumEpisodes=111,
                Year=2007,
                Actors= new List<string> {
                    "Jeffrey Donovan","Gabrielle Anwar","Bruce Campbell"
                }
            };
            Show three = new Show() {
                Name="Space Force",
                NumEpisodes=10,
                Year=2020,
                Actors= new List<string> {
                    "Steve Carrel","Ben Schwartz","John Malkovich"
                }
            };
            List<Show> shows = new List<Show>(){
                one, two, three
            };
            foreach (Show s in shows){
                Console.WriteLine(s);
            }

            Console.WriteLine("---------");
            shows.Sort();
            foreach (Show s in shows){
                Console.WriteLine(s);
            }

            Console.WriteLine("---------");
            shows.Sort(new NumEpisodeComparer());
            foreach (Show s in shows){
                Console.WriteLine(s);
            }

        }
    }
    public class NumEpisodeComparer : IComparer<Show>{
        public int Compare(Show x, Show y){
            return x.NumEpisodes-y.NumEpisodes;
        }
    }
}