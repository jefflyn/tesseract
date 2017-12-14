
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;


public class Cost {

	public static void main(String[] args) {
		if(args.length < 5){
			System.out.println("Invalid args! Correct format: [cost,share,price,share,isSh(0|1)]");
		}else{
			try{
			double cost = Double.valueOf(args[0]);
			int share = Integer.valueOf(args[1]);
			double price = Double.valueOf(args[2]);
			int buyShare = Integer.valueOf(args[3]);
			int isSh = Integer.valueOf(args[4]);
			int actFee = 0;
			if(isSh == 1 && buyShare > 0)
				actFee = (buyShare > 1000) ? (buyShare % 1000 == 0 ? buyShare / 1000 : buyShare / 1000 + 1) : 1;
			double feeRate = 0.00025;
			double dealAmt = price * buyShare;
			double dealFee = dealAmt * feeRate;
			if(dealFee <= 5 && buyShare > 0)
				dealFee = 5;
			
			double totalAmt = cost * share + price * buyShare + dealFee + actFee;
			double newCost = totalAmt / (share + buyShare);
			if(args.length > 5 && "y".equals(args[5])){
				System.out.println("(" + cost + "*" + share + "+" + price + "*" + buyShare + "+" + dealFee + "+" + actFee +")/(" + share + "+" + buyShare + ")=" + newCost);
			}
			System.out.println("Final cost: " + newCost);
			System.out.println("Total amount: " + totalAmt);
			System.out.println("Total tax: " + (totalAmt * 0.001));
			String fs = String.format("%.2f", (newCost -  price) / price * 100);
			System.out.println("Loss percent: " +  fs + "%");
			}catch(Exception e){
				System.err.println("Invalid args! Correct format: [cost,share,price,share,isSh(0|1)]");
				System.exit(1);
			}
		}
	}
}
