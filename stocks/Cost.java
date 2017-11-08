
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;


public class Cost {

	public static void main(String[] args) {
		if(args.length < 5){
			System.out.println("Invalid args! Correct format: [cost,share,price,share,isSh(0|1)]");
		}else{
			double cost = Double.valueOf(args[0]);
			int share = Integer.valueOf(args[1]);
			double price = Double.valueOf(args[2]);
			int buyShare = Integer.valueOf(args[3]);
			int isSh = Integer.valueOf(args[4]);
			int actFee = 0;
			if(isSh == 1)
				actFee = (buyShare > 1000) ? (buyShare / 1000 + 1) : 1;
			double feeRate = 0.00025;
			double dealAmt = price * buyShare;
			double dealFee = dealAmt * feeRate;
			if(dealFee <= 5)
				dealFee = 5;
			
			double totalAmt = cost * share + price * buyShare + dealFee + actFee;
			double newCost = totalAmt / (share + buyShare);
			System.out.println("(" + cost + "*" + share + "+" + price + "*" + buyShare + "+" + dealFee + "+" + actFee +")/(" + share + "+" + buyShare + ")=" + newCost);
			System.out.println("total amount: " + totalAmt);
			System.out.println("tax: " + (totalAmt * 0.0001));
		}
	}
}
