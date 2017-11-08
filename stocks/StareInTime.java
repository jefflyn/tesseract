
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.Set;
import java.util.TreeMap;

public class StareInTime {

	public static void main(String[] args) throws InterruptedException, IOException {

		InputStream in = StareInTime.class.getClassLoader().getResourceAsStream("config.properties");
		Properties pro = new Properties();
		if(in == null){
			pro.put("interval", 5*1000);
			pro.put("sh000001", "3200");
		}else{
			pro.load(in);
		}
		int time = pro.get("interval") == null ? 5 : Integer.valueOf(String.valueOf(pro.get("interval")));
		pro.remove("interval");

		Set<Map.Entry<Object, Object>> proSet =  pro.entrySet();
		Iterator<Entry<Object, Object>> it = proSet.iterator();

		Map<String, String> stocks = new HashMap<>();
		StringBuilder reqParams = new StringBuilder("q=");
		while(it.hasNext()){
			Entry<Object, Object> stock = it.next();
			String code = String.valueOf(stock.getKey());
			String cost = String.valueOf(stock.getValue());
			stocks.put(code, cost);

//			String prefix = "";
//			if(code.startsWith("6")){
//				prefix = "sh";
//			}else if(code.startsWith("0")){
//				prefix = "sz";
//			}
			reqParams.append(code + ",");
		}

		while (true) {
			// 发送 GET 请求
			String respStr = StareInTime.sendGet("http://qt.gtimg.cn", reqParams.toString());
			String[] stockArr = respStr.split(";");

			Map<Double, String> result = new TreeMap<>();
         List<String> indexList = new ArrayList<>();
			for(int i = 0; i < stockArr.length; i++){
				String[] info = stockArr[i].split("=");
				if(info.length != 2) continue;
				String stockey = info[0];
				String stockContent = info[1];
				//stock detail
				String[] attrs = stockContent.split("~");
				String name = attrs[1];
				String code = attrs[2];
				String price = attrs[3];
				String costQty = stocks.get(stockey.split("_")[1]);
				String cost = costQty.split(",")[0];
				String qty = "0";
				if(costQty.contains(",")){
					qty = "".equals(costQty.split(",")[1]) ? "0" : costQty.split(",")[1];
				}
				double diff = Double.valueOf(price) - Double.valueOf(cost);
				double balance = diff * Double.valueOf(qty);
				Double ratio = Double.valueOf(attrs[32]);
				String prefix = "";
				String post = ratio >= 0 ? "↑" : "↓";
				if("sh000001".equals(stockey.split("_")[1]) || "sz399001".equals(stockey.split("_")[1])){
					if(diff < 0){
						prefix = "!!!";
					}
               String indexInfo = prefix + " <<< " + code + " (" + price + ", " + cost + ", "
					        + String.format("%.2f", diff) + ") " + ratio + "%" + post + " " + attrs[33] + " "
					        + attrs[34] + " >>>";
               indexList.add(indexInfo);
					//firstly print the bellwether(very important)
					//System.out.println();
					//System.out.println("--------------------------------------------------------");
					continue;
				}else{
					if(diff < 0){
						prefix = "!";
					}
					if(diff > 0 && balance > 30){
						prefix = "$";
					}
				}
				
				String content = prefix + " " + code + " (" + price + ", " + cost + ", "
				        + String.format("%.2f", diff) + ", " + String.format("%.2f", balance) + ", "+ String.format("%.2f", diff / Double.valueOf(cost) * 100) + "%" + ") "
						+ ratio + "%" + post + " " + attrs[33] + " " + attrs[34];
				result.put(ratio, content);
			}
			List<String> col = new ArrayList<>(result.values());
			//for(int i = col.size() - 1; i > -1; i--){
			for(int i = 0; i < col.size(); i++){
				System.out.println(col.get(i));
				if(i < col.size())
					System.out.println("--------------------------------------------------------");
			}
         for(String s : indexList){
            System.out.println(s);        
         }

			//System.out.println("========================================================");
			Thread.sleep(time * 1000);
		}
	}

	/**
	 * 向指定URL发送GET方法的请求
	 *
	 * @param url
	 *            发送请求的URL
	 * @param param
	 *            请求参数，请求参数应该是 name1=value1&name2=value2 的形式。
	 * @return URL 所代表远程资源的响应结果
	 */
	public static String sendGet(String url, String param) {
		String result = "";
		BufferedReader in = null;
		try {
			String urlNameString = url + "/" + param;
			//System.out.println(urlNameString);
			URL realUrl = new URL(urlNameString);
			// 打开和URL之间的连接
			URLConnection connection = realUrl.openConnection();
			// 设置通用的请求属性
			connection.setRequestProperty("accept", "*/*");
			connection.setRequestProperty("connection", "Keep-Alive");
			connection.setRequestProperty("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)");
			// 建立实际的连接
			connection.connect();
			// 获取所有响应头字段
//			Map<String, List<String>> map = connection.getHeaderFields();
//			//遍历所有的响应头字段
//			for (String key : map.keySet()) {
//				System.out.println(key + "--->" + map.get(key));
//			}
			//定义 BufferedReader输入流来读取URL的响应
			in = new BufferedReader(new InputStreamReader(connection.getInputStream(), "GBK"));
			String line;
			while ((line = in.readLine()) != null) {
				result += line;
			}
		} catch (Exception e) {
			System.out.println("发送GET请求出现异常！" + e);
			e.printStackTrace();
		}
		// 使用finally块来关闭输入流
		finally {
			try {
				if (in != null) {
					in.close();
				}
			} catch (Exception e2) {
				e2.printStackTrace();
			}
		}
		return result;
	}
}
