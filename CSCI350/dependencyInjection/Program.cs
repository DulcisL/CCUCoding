//Somewhere it would tell to use the betterTransfer 2.0 when ItransferService is called (Injection)
ITransferService, BetterTransfers2p0 //You would only have to change it in that one spot

//Main
Console.WriteLine("Hello, World!");
Course c = new Course ("CSCI 300");
c.getCourseEquivalent("Penn State");


public class Course {
    public string Name;

    private MyTransfer transferService;

    public Course(string Name, ITransferService myTransfer){
        this.Name = Name;
        transferService = myTransfer;
    }

    public getCourseEquivalent(string University){
        return transfer.getEquivalent(Name, University);

    }
    
}

public class MyTransfer:ITransferService{
    public string getEquivalent(string courseName, string universityName1){
        return "";
    }
}

public class BetterTransfers:ITransferService{
    public string getEquivalent(string courseName, string universityName1){
        return "";
    }
}
public class BetterTransfers2p0:ITransferService{
    public string getEquivalent(string courseName, string universityName1){
        return "";
    }
}

public interface ITransferService{
    public string getEquivalent(string courseName, string university);
}