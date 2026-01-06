
const DATA_MAP = {
  "1": {
    "title": "JVM\u8fd0\u884c\u65f6\u5185\u5b58\u7ed3\u6784",
    "style": "background-color: yellow;",
    "details": "",
    "subItems": []
  },
  "2": {
    "title": "Java\u5185\u5b58\u7ba1\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "3": {
    "title": "\u5783\u573e\u56de\u6536\u7b97\u6cd5\u4ecb\u7ecd",
    "style": "",
    "details": "\u6309\u201c\u603b\u7ed3 \u2192 \u6982\u5ff5\u539f\u7406 \u2192 \u4f18\u7f3a\u70b9/\u573a\u666f \u2192 \u5e38\u89c1\u5751&\u89e3\u6cd5\u201d\u8bb2 JVM \u5783\u573e\u56de\u6536\u7b97\u6cd5\u3002\n\n## 1\uff09\u603b\u7ed3\nGC\u7b97\u6cd5\u6838\u5fc3\u5c31\u4e24\u7c7b\u601d\u8def\uff1a  \n- **\u6807\u8bb0\u7c7b**\uff1a\u5148\u627e\u201c\u6d3b\u7684\u201d\uff0c\u5176\u4f59\u56de\u6536\uff08\u6807\u8bb0-\u6e05\u9664 / \u6807\u8bb0-\u6574\u7406 / \u6807\u8bb0-\u590d\u5236\uff09  \n- **\u5f15\u7528\u8ba1\u6570\u7c7b**\uff1a\u9760\u8ba1\u6570\u589e\u51cf\u5224\u65ad\uff08Java\u4e3b\u6d41\u4e0d\u7528\u505a\u4e3b\u7b97\u6cd5\uff09  \n\u518d\u7ed3\u5408**\u5206\u4ee3\u5047\u8bbe**\uff1a\u65b0\u751f\u4ee3\u201c\u671d\u751f\u5915\u6b7b\u201d\u7528\u590d\u5236\u66f4\u5212\u7b97\uff0c\u8001\u5e74\u4ee3\u201c\u5b58\u6d3b\u7387\u9ad8\u201d\u7528\u6807\u8bb0\u6574\u7406/\u6e05\u9664\u66f4\u5408\u9002\u3002\n\n---\n\n## 2\uff09\u6982\u5ff5\u539f\u7406\uff08\u7b97\u6cd5\u600e\u4e48\u505a\uff09\n### 2.1 \u53ef\u8fbe\u6027\u5206\u6790\uff08GC Roots\uff09\nJava\u5224\u65ad\u5bf9\u8c61\u662f\u5426\u201c\u5783\u573e\u201d\uff0c\u4e3b\u6d41\u7528**\u53ef\u8fbe\u6027\u5206\u6790**\uff1a\u4ece GC Roots \u51fa\u53d1\u80fd\u8d70\u5230\u7684\u5bf9\u8c61\u90fd\u7b97\u6d3b\u3002  \n\u5e38\u89c1 Roots\uff1a\u7ebf\u7a0b\u6808\u5f15\u7528\u3001\u9759\u6001\u53d8\u91cf\u5f15\u7528\u3001JNI\u5f15\u7528\u3001\u8fd0\u884c\u4e2d\u9501\u6301\u6709\u5bf9\u8c61\u7b49\u3002\n\n### 2.2 \u6807\u8bb0-\u6e05\u9664\uff08Mark-Sweep\uff09\n- **\u6b65\u9aa4**\uff1a\u6807\u8bb0\u5b58\u6d3b\u5bf9\u8c61 \u2192 \u6e05\u9664\u672a\u6807\u8bb0\u5bf9\u8c61\n- **\u7279\u70b9**\uff1a\u5b9e\u73b0\u7b80\u5355\uff1b\u4f46\u4f1a\u4ea7\u751f**\u5185\u5b58\u788e\u7247**\uff0c\u5206\u914d\u5927\u5bf9\u8c61\u53ef\u80fd\u5931\u8d25\u3002\n\n### 2.3 \u6807\u8bb0-\u6574\u7406\uff08Mark-Compact\uff09\n- **\u6b65\u9aa4**\uff1a\u6807\u8bb0\u5b58\u6d3b\u5bf9\u8c61 \u2192 \u628a\u5b58\u6d3b\u5bf9\u8c61\u5411\u4e00\u7aef\u201c\u6324\u538b\u201d \u2192 \u6e05\u7406\u8fb9\u754c\u5916\u5185\u5b58\n- **\u7279\u70b9**\uff1a\u89e3\u51b3\u788e\u7247\uff1b\u4ee3\u4ef7\u662f**\u6574\u7406\u79fb\u52a8\u5bf9\u8c61\u6210\u672c\u9ad8**\u3001\u505c\u987f\u53ef\u80fd\u66f4\u957f\u3002\u5e38\u7528\u4e8e\u8001\u5e74\u4ee3\u3002\n\n### 2.4 \u590d\u5236\u7b97\u6cd5\uff08Copying / Semi-space\uff09\n- **\u6b65\u9aa4**\uff1a\u628a\u5b58\u6d3b\u5bf9\u8c61\u4ece From \u590d\u5236\u5230 To \u2192 \u76f4\u63a5\u6e05\u7a7a From\n- **\u7279\u70b9**\uff1a\u5206\u914d\u5feb\u3001\u65e0\u788e\u7247\uff1b\u7f3a\u70b9\u662f\u9700\u8981**\u989d\u5916\u4e00\u5757\u540c\u7b49\u7a7a\u95f4**\u3002\u65b0\u751f\u4ee3\u5e38\u7528\uff08Eden + Survivor\uff09\u3002\n\n### 2.5 \u5206\u4ee3\u6536\u96c6\uff08Generational\uff09\n- \u65b0\u751f\u4ee3\uff1a\u590d\u5236 + \u5feb\u901f\u56de\u6536\uff08Minor GC / Young GC\uff09\n- \u8001\u5e74\u4ee3\uff1a\u6807\u8bb0-\u6e05\u9664/\u6574\u7406\uff08Major/Old GC\uff09\n- \u8de8\u4ee3\u5f15\u7528\u7528 **\u8bb0\u5fc6\u96c6/\u5361\u8868** \u964d\u4f4e\u626b\u63cf\u6210\u672c\uff08\u907f\u514d\u6bcf\u6b21\u90fd\u626b\u6574\u4e2a\u8001\u5e74\u4ee3\uff09\u3002\n\n### 2.6 \u5f15\u7528\u8ba1\u6570\uff08Reference Counting\uff0c\u4e3a\u4f55Java\u4e0d\u4e3b\u7528\uff09\n- **\u4f18\u70b9**\uff1a\u56de\u6536\u53ca\u65f6\u3001\u5b9e\u73b0\u76f4\u89c2\n- **\u81f4\u547d\u95ee\u9898**\uff1a\u65e0\u6cd5\u89e3\u51b3**\u5faa\u73af\u5f15\u7528**\uff08A\u5f15\u7528B\uff0cB\u5f15\u7528A\uff0c\u8ba1\u6570\u90fd\u4e0d\u4e3a0\uff09\u3002\n\n---\n\n## 3\uff09\u4f18\u7f3a\u70b9 & \u9002\u7528\u573a\u666f\uff08\u600e\u4e48\u9009\uff09\n- **\u590d\u5236**\uff1a\u9002\u5408\u5b58\u6d3b\u7387\u4f4e\u3001\u5bf9\u8c61\u5c0f\u4e14\u591a\u7684\u533a\u57df\uff08\u65b0\u751f\u4ee3\uff09\u3002\n- **\u6807\u8bb0-\u6574\u7406**\uff1a\u9002\u5408\u5b58\u6d3b\u7387\u9ad8\u3001\u5e0c\u671b\u65e0\u788e\u7247\u7684\u533a\u57df\uff08\u8001\u5e74\u4ee3\u3001\u9700\u8981\u8fde\u7eed\u7a7a\u95f4\u65f6\uff09\u3002\n- **\u6807\u8bb0-\u6e05\u9664**\uff1a\u9002\u5408\u5bf9\u505c\u987f\u66f4\u654f\u611f\u3001\u80fd\u5bb9\u5fcd\u788e\u7247\u6216\u6709\u914d\u5957\uff08\u5982\u7a7a\u95f2\u5217\u8868\uff09\u7684\u573a\u666f\uff08\u90e8\u5206\u8001\u5e74\u4ee3\u5b9e\u73b0\u4f1a\u7528\uff09\u3002\n\n> \u5b9e\u9645\u4e0a\u4f60\u7528 G1/ZGC \u8fd9\u7c7b\u6536\u96c6\u5668\u65f6\uff0c\u5e95\u5c42\u4ecd\u662f\u8fd9\u4e9b\u7b97\u6cd5\u7684\u7ec4\u5408\u4e0e\u5de5\u7a0b\u5316\u5b9e\u73b0\uff08\u5e76\u53d1\u6807\u8bb0\u3001\u5206\u533a\u3001\u8f6c\u79fb\u7b49\uff09\u3002\n\n---\n\n## 4\uff09\u5e38\u89c1\u5751 & \u89e3\u51b3\u65b9\u6848\n1) **\u8001\u5e74\u4ee3\u788e\u7247\u5bfc\u81f4 Full GC \u9891\u7e41/\u5206\u914d\u5931\u8d25**  \n- \u73b0\u8c61\uff1a\u8001\u5e74\u4ee3\u660e\u660e\u8fd8\u6709\u7a7a\u95f4\u4f46\u5206\u914d\u5927\u5bf9\u8c61\u5931\u8d25\u89e6\u53d1 Full GC  \n- \u89e3\u6cd5\uff1a\u503e\u5411\u4f7f\u7528\u5e26\u6574\u7406/\u538b\u7f29\u80fd\u529b\u7684\u7b56\u7565\uff08\u5982G1\u7684\u8f6c\u79fb/\u538b\u7f29\u7279\u6027\uff09\uff1b\u51cf\u5c11\u5927\u5bf9\u8c61\u76f4\u63a5\u8fdb\u8001\u5e74\u4ee3\uff1b\u5408\u7406\u8bbe\u7f6e\u5806\u4e0e\u664b\u5347\u9608\u503c\n\n2) **\u664b\u5347\u5931\u8d25\uff08promotion failed\uff09**\uff08\u65b0\u751f\u4ee3\u590d\u5236\u5230\u8001\u5e74\u4ee3\u653e\u4e0d\u4e0b\uff09  \n- \u89e3\u6cd5\uff1a\u589e\u5927\u8001\u5e74\u4ee3/\u5806\uff1b\u964d\u4f4e\u5bf9\u8c61\u5b58\u6d3b\u7387\uff08\u51cf\u5c11\u957f\u751f\u547d\u5468\u671f\u7f13\u5b58\uff09\uff1b\u8c03\u6574 Survivor \u6bd4\u4f8b\u4e0e\u664b\u5347\u7b56\u7565\n\n3) **Minor GC\u5f88\u9891\u7e41**\uff08\u5206\u914d\u8fc7\u5feb\u3001Eden\u592a\u5c0f\uff09  \n- \u89e3\u6cd5\uff1a\u589e\u5927\u65b0\u751f\u4ee3\u6216\u4f18\u5316\u5bf9\u8c61\u521b\u5efa\uff08\u590d\u7528\u3001\u6c60\u5316\u8981\u8c28\u614e\uff09\uff1b\u6392\u67e5\u77ed\u751f\u547d\u5468\u671f\u5927\u5bf9\u8c61\n\n4) **\u628a\u201c\u5f15\u7528\u7c7b\u578b\u201d\u5f53\u7b97\u6cd5**  \n- \u5f3a/\u8f6f/\u5f31/\u865a\u5f15\u7528\u662f\u201c\u5bf9\u8c61\u53ef\u8fbe\u6027\u5f3a\u5f31\u201d\uff0c\u4e0d\u662fGC\u7b97\u6cd5\uff1b\u5e38\u7528\u4e8e\u7f13\u5b58\uff08Soft\uff09\u3001\u89c4\u8303\u5316\u6620\u5c04/\u5f31\u952e\uff08Weak\uff09\u7b49\u3002\n\n\u5982\u679c\u4f60\u9762\u8bd5\u9700\u8981\u518d\u5f80\u4e0b\u63a5\uff0c\u6211\u53ef\u4ee5\u628a\u8fd9\u4e9b\u7b97\u6cd5\u600e\u4e48\u5bf9\u5e94\u5230 **Serial/Parallel/CMS/G1/ZGC** \u4ee5\u53ca\u5404\u81ea\u89e6\u53d1\u6761\u4ef6\u3001\u505c\u987f\u7279\u5f81\uff0c\u4e32\u6210\u4e00\u5957\u8bdd\u672f\u3002",
    "subItems": []
  },
  "4": {
    "title": "\u5783\u573e\u56de\u6536\u5668\u4ecb\u7ecd\u4ee5\u53cajdk",
    "style": "",
    "details": "",
    "subItems": []
  },
  "5": {
    "title": "Java\u5783\u573e\u56de\u6536\u673a\u5236",
    "style": "",
    "details": "",
    "subItems": [
      "JVM\u7684\u6c38\u4e45\u4ee3\u4e2d\u4f1a\u53d1\u751f\u5783\u573e\u56de\u6536\u4e48\uff1f",
      "Minor GC\u4e0eFull GC\u5206\u522b\u5728\u4ec0\u4e48\u65f6\u5019\u53d1\u751f\uff1f"
    ]
  },
  "6": {
    "title": "Full GC\u548cMinor GC",
    "style": "",
    "details": "",
    "subItems": []
  },
  "7": {
    "title": "OOM\u7684\u7c7b\u578b\uff0c\u4e3b\u8981\u539f\u56e0\u548c\u6392\u67e5",
    "style": "",
    "details": "",
    "subItems": []
  },
  "8": {
    "title": "Java\u6027\u80fd\u4f18\u5316\u51cf\u5c11GC",
    "style": "",
    "details": "",
    "subItems": []
  },
  "9": {
    "title": "JVM\u7c7b\u52a0\u8f7d\u539f\u7406\u548c\u8fc7\u7a0b",
    "style": "",
    "details": "",
    "subItems": []
  },
  "10": {
    "title": "Java\u7ebf\u7a0b\u6a21\u578bJMM",
    "style": "",
    "details": "",
    "subItems": []
  },
  "11": {
    "title": "JDK8\u7684\u65b0\u7279\u6027",
    "style": "",
    "details": "",
    "subItems": []
  },
  "17": {
    "title": "Java\u96c6\u5408",
    "style": "",
    "details": "",
    "subItems": []
  },
  "18": {
    "title": "HashMap\u4ecb\u7ecd",
    "style": "",
    "details": "",
    "subItems": []
  },
  "19": {
    "title": "Java\u7ebf\u7a0b\u548c\u751f\u547d\u5468\u671f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "20": {
    "title": "\u7ec8\u6b62\u7ebf\u7a0b\u7684\u65b9\u5f0f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "21": {
    "title": "\u7ebf\u7a0b\u95f4\u600e\u4e48\u901a\u8baf",
    "style": "",
    "details": "",
    "subItems": []
  },
  "22": {
    "title": "\u7ebf\u7a0b\u6c60\u539f\u7406\u4ee5\u53ca\u8c03\u4f18",
    "style": "",
    "details": "",
    "subItems": []
  },
  "23": {
    "title": "Java\u9501\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "24": {
    "title": "\u7ebf\u7a0b\u5171\u4eab",
    "style": "",
    "details": "",
    "subItems": []
  },
  "25": {
    "title": "ThreadLocal\u548cThreadLocalMap",
    "style": "",
    "details": "",
    "subItems": []
  },
  "26": {
    "title": "synchronized",
    "style": "",
    "details": "",
    "subItems": []
  },
  "27": {
    "title": "CAS\u548cAQS\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "28": {
    "title": "volatile\u7684\u4f5c\u7528",
    "style": "",
    "details": "",
    "subItems": []
  },
  "29": {
    "title": "Java\u53cd\u5c04\u539f\u7406\u548c\u5e94\u7528",
    "style": "",
    "details": "",
    "subItems": []
  },
  "30": {
    "title": "Java\u5bf9\u8c61\u590d\u5236\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "31": {
    "title": "Spring IOC",
    "style": "",
    "details": "",
    "subItems": []
  },
  "32": {
    "title": "Spring AOP",
    "style": "",
    "details": "",
    "subItems": []
  },
  "33": {
    "title": "Spring\u751f\u547d\u5468\u671f\u7ba1\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "34": {
    "title": "Spring\u600e\u4e48\u89e3\u51b3\u5faa\u73af\u4f9d\u8d56",
    "style": "",
    "details": "",
    "subItems": []
  },
  "35": {
    "title": "Spring\u4ee3\u7406\u6a21\u5f0f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "36": {
    "title": "Spring\u5e38\u89c1\u8bbe\u8ba1\u6a21\u5f0f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "37": {
    "title": "Spring\u4e8b\u52a1\u7ba1\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "38": {
    "title": "BeanFactory\u548cFactoryBean",
    "style": "",
    "details": "",
    "subItems": []
  },
  "39": {
    "title": "SpringMVC\u5de5\u4f5c\u6d41\u7a0b",
    "style": "",
    "details": "",
    "subItems": []
  },
  "40": {
    "title": "\u6ce8\u89e3\u5931\u6548\u539f\u7406\u4ee5\u53ca\u89e3\u51b3",
    "style": "",
    "details": "",
    "subItems": []
  },
  "41": {
    "title": "SpringBoot\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "42": {
    "title": "MyBatis\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "43": {
    "title": "MyBatis\u7f13\u5b58\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "44": {
    "title": "MyBatis\u9047\u5230\u7684\u5751",
    "style": "",
    "details": "",
    "subItems": []
  },
  "45": {
    "title": "SpringBoot Starter\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "52": {
    "title": "\u6570\u636e\u5e93\u4e8b\u52a1\u4ecb\u7ecd",
    "style": "",
    "details": "",
    "subItems": []
  },
  "53": {
    "title": "SQL\u6267\u884c\u8fc7\u7a0b",
    "style": "",
    "details": "",
    "subItems": []
  },
  "54": {
    "title": "\u6570\u636e\u5e93\u9501\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "55": {
    "title": "\u805a\u7c07\u7d22\u5f15\u4ecb\u7ecd",
    "style": "",
    "details": "",
    "subItems": []
  },
  "56": {
    "title": "MySQL\u7d22\u5f15\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "57": {
    "title": "\u5199\u591a\u8bfb\u5c11\u65b9\u6848",
    "style": "",
    "details": "",
    "subItems": []
  },
  "58": {
    "title": "\u60b2\u89c2\u9501\u548c\u4e50\u89c2\u9501",
    "style": "",
    "details": "",
    "subItems": []
  },
  "59": {
    "title": "\u6b7b\u9501\u6392\u67e5\u548c\u89e3\u51b3",
    "style": "",
    "details": "",
    "subItems": []
  },
  "60": {
    "title": "\u6162SQL\u4f18\u5316",
    "style": "",
    "details": "",
    "subItems": []
  },
  "61": {
    "title": "\u6267\u884c\u8ba1\u5212\u600e\u4e48\u770b",
    "style": "",
    "details": "",
    "subItems": []
  },
  "62": {
    "title": "\u5206\u5e03\u5f0f\u4e8b\u52a1\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "63": {
    "title": "\u5206\u5e03\u5f0f\u4e8b\u52a1\u89e3\u51b3\u65b9\u6848",
    "style": "",
    "details": "",
    "subItems": []
  },
  "64": {
    "title": "Redis\u4e3a\u4ec0\u4e48\u6027\u80fd\u9ad8",
    "style": "",
    "details": "",
    "subItems": []
  },
  "65": {
    "title": "Redis\u6301\u4e45\u5316\u7b56\u7565",
    "style": "",
    "details": "",
    "subItems": []
  },
  "66": {
    "title": "Redis\u9ad8\u53ef\u7528\u548c\u96c6\u7fa4\u65b9\u5f0f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "67": {
    "title": "\u7f13\u5b58\u600e\u4e48\u4fdd\u8bc1\u6570\u636e\u4e00\u81f4\u6027",
    "style": "",
    "details": "",
    "subItems": []
  },
  "89": {
    "title": "\u5fae\u670d\u52a1 \u80cc\u666f \u4f18\u7f3a\u70b9",
    "style": "",
    "details": "",
    "subItems": []
  },
  "90": {
    "title": "\u5fae\u670d\u52a1\u62c6\u5206\u539f\u5219",
    "style": "",
    "details": "",
    "subItems": []
  },
  "91": {
    "title": "\u670d\u52a1\u6ce8\u518c\u4e0e\u53d1\u73b0 Eureka+Nacos",
    "style": "",
    "details": "",
    "subItems": []
  },
  "92": {
    "title": "\u9650\u6d41 \u7194\u65ad \u964d\u7ea7\u600e\u4e48\u505a",
    "style": "",
    "details": "",
    "subItems": []
  },
  "93": {
    "title": "\u5fae\u670d\u52a1\u8d1f\u8f7d\u5747\u8861\u600e\u4e48\u505a",
    "style": "",
    "details": "",
    "subItems": []
  },
  "94": {
    "title": "CAP\u548cBASE\u7406\u8bba",
    "style": "",
    "details": "",
    "subItems": []
  },
  "95": {
    "title": "Nacos\u914d\u7f6e\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "96": {
    "title": "\u94fe\u8def \u670d\u52a1\u7f51\u5173\u8def\u7531\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "97": {
    "title": "RPC\u539f\u7406\u548c\u5b9e\u73b0\u6846\u67b6",
    "style": "",
    "details": "",
    "subItems": []
  },
  "98": {
    "title": "Zookeeper\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "99": {
    "title": "\u4e00\u81f4\u6027\u7b97\u6cd5\u6709\u54ea\u4e9b",
    "style": "",
    "details": "",
    "subItems": []
  },
  "100": {
    "title": "\u5982\u4f55\u4fdd\u8bc1\u63a5\u53e3\u5e42\u7b49",
    "style": "",
    "details": "",
    "subItems": []
  },
  "101": {
    "title": "\u5206\u5e03\u5f0f\u7f13\u5b58\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": []
  },
  "102": {
    "title": "\u5206\u5e03\u5f0fID\u751f\u6210",
    "style": "",
    "details": "",
    "subItems": []
  },
  "103": {
    "title": "\u5206\u5e03\u5f0f\u9501\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "104": {
    "title": "\u5206\u5e03\u5f0f\u4e8b\u52a1\u539f\u74062",
    "style": "",
    "details": "",
    "subItems": []
  },
  "105": {
    "title": "\u6d88\u606f\u961f\u5217\u7684\u4f7f\u7528\u573a\u666f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "106": {
    "title": "Kafka\u4e3a\u4ec0\u4e48\u9ad8\u6027\u80fd",
    "style": "",
    "details": "",
    "subItems": []
  },
  "107": {
    "title": "RocketMQ\u7684\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "108": {
    "title": "RocketMQ\u6d88\u606f\u4e8b\u52a1\u539f\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "109": {
    "title": "RocketMQ\u548cKafka\u9009\u578b\u5bf9\u6bd4",
    "style": "",
    "details": "",
    "subItems": []
  },
  "110": {
    "title": "\u4ecb\u7ecd\u9879\u76ee \u5171\u4eab\u5145\u7535\u5b9d",
    "style": "",
    "details": "",
    "subItems": [
      "\u4f60\u7684\u804c\u8d23\u548c\u5de5\u4f5c\u5185\u5bb9",
      "\u8be6\u7ec6\u8bb2\u4e00\u4e0b\u6280\u672f\u67b6\u6784",
      "\u600e\u4e48\u505a\u6280\u672f\u9009\u578b\uff1f\u4fdd\u8bc1\u9ad8\u6027\u80fd \u9ad8\u53ef\u7528",
      "\u4e3a\u4ec0\u4e48\u8fd9\u6837\u8bbe\u8ba1\uff1f",
      "\u9879\u76ee\u54ea\u4e9b\u5730\u65b9\u53ef\u6539\u8fdb\uff1f"
    ]
  },
  "111": {
    "title": "\u4ee3\u7801\u91cd\u6784\u600e\u4e48\u505a",
    "style": "",
    "details": "",
    "subItems": []
  },
  "112": {
    "title": "\u600e\u4e48\u505a\u6280\u672f\u9009\u578b",
    "style": "",
    "details": "",
    "subItems": []
  },
  "113": {
    "title": "\u7cfb\u7edf\u6027\u80fd\u4f18\u5316\u600e\u4e48\u505a",
    "style": "",
    "details": "",
    "subItems": []
  },
  "114": {
    "title": "\u7ebf\u4e0a\u95ee\u9898\u600e\u4e48\u89e3\u51b3",
    "style": "",
    "details": "",
    "subItems": []
  },
  "115": {
    "title": "code review\u548c\u8d28\u91cf\u7ba1\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "116": {
    "title": "\u7814\u53d1\u89c4\u8303",
    "style": "",
    "details": "",
    "subItems": []
  },
  "117": {
    "title": "\u67b6\u6784\u8bc4\u5ba1\u600e\u4e48\u505a",
    "style": "",
    "details": "",
    "subItems": []
  },
  "118": {
    "title": "\u5fae\u670d\u52a1\u7cfb\u7edf\u76d1\u63a7",
    "style": "",
    "details": "",
    "subItems": []
  },
  "119": {
    "title": "\u6d77\u91cf\u6570\u636e\u5e93\u8868\u5207\u6362\u65b9\u6848",
    "style": "",
    "details": "",
    "subItems": []
  },
  "120": {
    "title": "\u5982\u4f55\u5e94\u5bf9\u7a81\u53d1\u6d41\u91cf",
    "style": "",
    "details": "",
    "subItems": []
  },
  "121": {
    "title": "\u9ad8\u5e76\u53d1\u7cfb\u7edf\u74f6\u9888",
    "style": "",
    "details": "",
    "subItems": []
  },
  "122": {
    "title": "\u5f3a\u4e00\u81f4\u6027\u65b9\u6848",
    "style": "",
    "details": "",
    "subItems": []
  },
  "123": {
    "title": "\u6700\u7ec8\u4e00\u81f4\u6027\u65b9\u6848",
    "style": "",
    "details": "",
    "subItems": []
  },
  "124": {
    "title": "\u7cfb\u7edf\u96ea\u5d29\u5904\u7406\u65b9\u6848",
    "style": "",
    "details": "",
    "subItems": []
  },
  "125": {
    "title": "\u6392\u67e5\u4e00\u6b21\u8de8\u591a\u4e2a\u670d\u52a1\u7684\u6162\u8bf7\u6c42",
    "style": "",
    "details": "",
    "subItems": []
  },
  "126": {
    "title": "\u6d88\u606f\u79ef\u538b\u5982\u4f55\u5904\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "127": {
    "title": "\u5982\u4f55\u4fdd\u8bc1\u6d88\u606f\u4e0d\u4e22\u3001\u4e0d\u91cd\u3001\u4e0d\u4e71",
    "style": "",
    "details": "",
    "subItems": []
  },
  "128": {
    "title": "\u591a\u7ea7\u7f13\u5b58\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": []
  },
  "129": {
    "title": "\u7f13\u5b58\u95ee\u9898\u5904\u7406",
    "style": "",
    "details": "",
    "subItems": []
  },
  "130": {
    "title": "\u9ad8\u5e76\u53d1\u652f\u4ed8\u7cfb\u7edf\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": []
  },
  "131": {
    "title": "\u79d2\u6740\u7cfb\u7edf\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": []
  },
  "132": {
    "title": "\u9ad8\u5e76\u53d1\u8ba2\u5355\u7cfb\u7edf\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": []
  },
  "133": {
    "title": "\u5206\u5e93\u5206\u8868 \u573a\u666f\u548c\u65b9\u6848",
    "style": "",
    "details": "",
    "subItems": []
  },
  "134": {
    "title": "\u7cfb\u7edf\u8bbe\u8ba1\u539f\u5219\u548c\u8003\u91cf\u70b9",
    "style": "",
    "details": "",
    "subItems": []
  },
  "135": {
    "title": "DDD\u8bbe\u8ba1\u4ecb\u7ecd",
    "style": "",
    "details": "",
    "subItems": []
  },
  "136": {
    "title": "\u600e\u4e48\u63d0\u9ad8\u7cfb\u7edf\u53ef\u6269\u5c55\u6027",
    "style": "",
    "details": "",
    "subItems": []
  },
  "137": {
    "title": "\u9ad8\u6027\u80fd\u9ad8\u5e76\u53d1\u7cfb\u7edf\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": []
  },
  "138": {
    "title": "\u53d1\u5e03\u65b9\u5f0f\u548c\u90e8\u7f72\u5468\u671f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "139": {
    "title": "\u7cfb\u7edf\u600e\u4e48\u505a\u76d1\u63a7\u7684",
    "style": "",
    "details": "",
    "subItems": []
  },
  "140": {
    "title": "Docker\u548cK8S",
    "style": "",
    "details": "",
    "subItems": []
  },
  "141": {
    "title": "\u5fae\u670d\u52a1\u67b6\u6784\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": []
  },
  "142": {
    "title": "\u5982\u4f55\u7406\u89e3\u5927\u6a21\u578b",
    "style": "",
    "details": "",
    "subItems": [
      "\u548c\u4f20\u7edf\u7a0b\u5e8f\u7684\u533a\u522b\uff1f",
      "\u89e3\u91ca\u53c2\u6570 \u53c2\u6570\u89c4\u6a21 Token",
      "GPT\u3001LLaMA\u5927\u6a21\u578b\u9002\u5408\u505a\u4ec0\u4e48\uff1f"
    ]
  },
  "143": {
    "title": "AI\u548c\u540e\u7aef\u7cfb\u7edf\u7684\u5173\u7cfb",
    "style": "",
    "details": "",
    "subItems": []
  },
  "144": {
    "title": "\u5982\u4f55\u8bbe\u8ba1\u4e00\u4e2a\u57fa\u4e8eLLM\u7684\u540e\u7aef\u7cfb\u7edf",
    "style": "",
    "details": "",
    "subItems": []
  },
  "145": {
    "title": "\u7cfb\u7edf\u67b6\u6784\u548c\u6a21\u5757\u8bbe\u8ba1",
    "style": "",
    "details": "",
    "subItems": []
  },
  "146": {
    "title": "\u4ec0\u4e48\u662fAgent\u667a\u80fd\u4f53",
    "style": "",
    "details": "",
    "subItems": [
      "\u548c\u666e\u901aChat\u7684\u533a\u522b\uff1f",
      "Agent\u67b6\u6784"
    ]
  },
  "147": {
    "title": "RAG\u548c\u5411\u91cf\u6570\u636e\u5e93",
    "style": "",
    "details": "",
    "subItems": [
      "\u4e3a\u4ec0\u4e48\u9700\u8981RAG\u548c\u5411\u91cf\u6570\u636e\u5e93\uff1f",
      "\u5982\u4f55\u9009\u62e9\u5411\u91cf\u6570\u636e\u5e93\uff1f"
    ]
  },
  "148": {
    "title": "\u63d0\u793a\u5de5\u7a0b \u6838\u5fc3\u539f\u5219",
    "style": "",
    "details": "",
    "subItems": []
  },
  "149": {
    "title": "LangChain\u6846\u67b6",
    "style": "",
    "details": "",
    "subItems": []
  },
  "150": {
    "title": "FastGPT\u6982\u8ff0\u4e0e\u6838\u5fc3\u4ef7\u503c",
    "style": "",
    "details": "",
    "subItems": []
  },
  "151": {
    "title": "LLM\u4ea7\u751f\u5e7b\u89c9\u600e\u4e48\u907f\u514d",
    "style": "",
    "details": "",
    "subItems": []
  },
  "152": {
    "title": "Java\u5982\u4f55\u9ad8\u5e76\u53d1\u5b89\u5168\u8c03\u7528LLM",
    "style": "",
    "details": "",
    "subItems": []
  },
  "153": {
    "title": "\u5982\u4f55\u5728AI\u5e94\u7528\u4e2d\u505a\u7f13\u5b58",
    "style": "",
    "details": "",
    "subItems": []
  },
  "154": {
    "title": "AI\u670d\u52a1\u600e\u4e48\u505a\u76d1\u63a7\u548c\u6210\u672c\u63a7\u5236",
    "style": "",
    "details": "",
    "subItems": []
  },
  "155": {
    "title": "AI\u8f93\u51fa\u9020\u6210\u4e1a\u52a1\u5f71\u54cd\uff0c\u8c01\u8d1f\u8d23\uff1f",
    "style": "",
    "details": "",
    "subItems": [
      "\u7cfb\u7edf\u5982\u4f55\u8bbe\u8ba1\uff1f"
    ]
  },
  "156": {
    "title": "AI\u8de8\u884c\u4e1a\u7ecf\u9a8c\u590d\u5236\u4e0e\u5e94\u7528",
    "style": "",
    "details": "",
    "subItems": []
  },
  "157": {
    "title": "\u600e\u4e48\u770b\u5f85AI\u53d6\u4ee3\u7a0b\u5e8f\u5458",
    "style": "",
    "details": "",
    "subItems": []
  },
  "158": {
    "title": "\u81ea\u6211\u4ecb\u7ecd",
    "style": "",
    "details": "",
    "subItems": []
  },
  "159": {
    "title": "\u82f1\u6587\u53e3\u8bed\u81ea\u6211\u4ecb\u7ecd",
    "style": "",
    "details": "",
    "subItems": []
  },
  "160": {
    "title": "\u4e3a\u4ec0\u4e48\u60f3\u52a0\u5165\u6211\u4eec\u516c\u53f8\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "161": {
    "title": "\u80fd\u7ed9\u6211\u4eec\u5e26\u6765\u4ec0\u4e48\uff1f\u4e3a\u4ec0\u4e48\u96c7\u4f63\u4f60\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "162": {
    "title": "\u4e0a\u4efd\u5de5\u4f5c\u6700\u5927\u6536\u83b7\u662f\u4ec0\u4e48\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "163": {
    "title": "\u65b0\u52a0\u5165\u5bf9\u4f60\u6709\u4ec0\u4e48\u6311\u6218\uff1f\u600e\u4e48\u5f00\u5c55\u5de5\u4f5c\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "164": {
    "title": "\u5982\u679c\u52a0\u5165\u6211\u4eec\uff0c\u4f60\u5e0c\u671b\u505a\u54ea\u4e9b\u6311\u6218\u6027\u7684\u4e8b\u60c5\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "165": {
    "title": "\u4f60\u66f4\u504f\u6280\u672f\u6df1\u8015\uff0c\u8fd8\u662f\u613f\u610f\u8f6c\u7ba1\u7406\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "166": {
    "title": "\u4f60\u672a\u67653/5\u5e74\u7684\u804c\u4e1a\u76ee\u6807\u662f\u4ec0\u4e48\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "167": {
    "title": "\u4f60\u662f\u5982\u4f55\u5b89\u6392\u4e2a\u4eba\u6210\u957f\u65f6\u95f4\u7684\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "168": {
    "title": "\u4f60\u6700\u5927\u7684\u4f18\u70b9\u662f\u4ec0\u4e48\uff1f\u77ed\u677f\u6216\u5f85\u6539\u8fdb\u7684\u5730\u65b9\u662f\u4ec0\u4e48\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "169": {
    "title": "\u4f60\u5e26\u8fc7\u7684\u56e2\u961f\u89c4\u6a21\u662f\u591a\u5c11\uff1f\u5982\u4f55\u7ba1\u7406\u56e2\u961f\u7684\u6280\u672f\u6210\u957f\u548c\u4ea4\u4ed8\u8fdb\u5ea6\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "170": {
    "title": "\u5982\u4f55\u7ba1\u7406\u7814\u53d1\u56e2\u961f\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "171": {
    "title": "\u56e2\u961f\u7ba1\u7406\u600e\u4e48\u5206\u5de5\u534f\u4f5c\u4ee5\u53ca\u600e\u4e48\u5206\u914d\u4efb\u52a1\u80fd\u4fdd\u8bc1\u65b0\u4eba\u6210\u957f\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "172": {
    "title": "\u600e\u4e48\u8861\u91cf\u5458\u5de5\u7684\u7ee9\u6548\uff1f\u5982\u679c\u4e0b\u5c5e\u7ee9\u6548\u4e0d\u8fbe\u6807\uff0c\u600e\u4e48\u505aPIP",
    "style": "",
    "details": "",
    "subItems": []
  },
  "173": {
    "title": "\u5728\u4e00\u4e2a\u9879\u76ee\u4e2d\uff0c\u4f60\u662f\u5982\u4f55\u6743\u8861\u4e1a\u52a1\u9700\u6c42\u4e0e\u6280\u672f\u5b9e\u73b0\u7684\u590d\u6742\u5ea6\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "174": {
    "title": "\u9879\u76ee\u5ef6\u671f\u65f6\uff0c\u4f60\u4f1a\u600e\u4e48\u5411\u4e0a\u6c47\u62a5\u5e76\u534f\u8c03\u8d44\u6e90\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "175": {
    "title": "\u4f60\u662f\u66f4\u559c\u6b22\u72ec\u7acb\u5b8c\u6210\u4efb\u52a1\uff0c\u8fd8\u662f\u548c\u56e2\u961f\u534f\u4f5c\uff1f\u4e3a\u4ec0\u4e48\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "176": {
    "title": "\u9047\u5230\u4ea7\u54c1\u7ecf\u7406\u63d0\u51fa\u4e0d\u5408\u7406\u9700\u6c42\u65f6\uff0c\u4f60\u600e\u4e48\u6c9f\u901a\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "177": {
    "title": "\u6709\u6ca1\u6709\u9047\u5230\u8fc7\u7ebf\u4e0a\u4e8b\u6545\uff1f\u4f60\u662f\u600e\u4e48\u590d\u76d8\u548c\u63a8\u52a8\u6539\u8fdb\u7684\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "178": {
    "title": "\u8bf7\u8c08\u8c08\u4f60\u5728\u9879\u76ee\u4e2d\u662f\u5982\u4f55\u5f71\u54cd\u5176\u4ed6\u56e2\u961f\u7684\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "179": {
    "title": "\u4f60\u6709\u6ca1\u6709\u63a8\u52a8\u8fc7\u6280\u672f\u5347\u7ea7\u6216\u8005\u6280\u672f\u6808\u53d8\u66f4\uff1f\u662f\u5982\u4f55\u8bf4\u670d\u7ba1\u7406\u5c42\u7684\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  },
  "180": {
    "title": "\u5f53\u53d1\u73b0\u73b0\u6709\u7cfb\u7edf\u67b6\u6784\u9762\u4e34\u4e25\u91cd\u7684\u6280\u672f\u503a\uff0c\u4f46\u4e1a\u52a1\u4e0a\u7ebf\u538b\u529b\u5f88\u5927\uff0c\u4f60\u5982\u4f55\u9009",
    "style": "",
    "details": "",
    "subItems": []
  },
  "181": {
    "title": "\u4f60\u600e\u4e48\u770b\u5f85 996 \u6216\u9ad8\u5f3a\u5ea6\u5de5\u4f5c\uff1f\u600e\u6837\u5e73\u8861\u6548\u7387\u4e0e\u53ef\u6301\u7eed\u53d1\u5c55\uff1f",
    "style": "",
    "details": "",
    "subItems": []
  }
};
const DISPLAY_MAP = {
  "3": [
    [
      110,
      120,
      137,
      135,
      null,
      null
    ],
    [
      111,
      121,
      134,
      134,
      null,
      null
    ],
    [
      112,
      122,
      130,
      136,
      null,
      null
    ],
    [
      113,
      123,
      132,
      null,
      null,
      null
    ],
    [
      114,
      124,
      131,
      null,
      null,
      null
    ],
    [
      115,
      125,
      null,
      null,
      null,
      null
    ],
    [
      116,
      128,
      null,
      null,
      null,
      null
    ],
    [
      117,
      129,
      null,
      null,
      null,
      null
    ],
    [
      138,
      133,
      null,
      null,
      null,
      null
    ],
    [
      139,
      126,
      null,
      null,
      null,
      null
    ],
    [
      118,
      127,
      null,
      null,
      null,
      null
    ],
    [
      140,
      null,
      null,
      null,
      null,
      null
    ]
  ],
  "4": [
    [
      142,
      151,
      null,
      null,
      null,
      null
    ],
    [
      143,
      153,
      null,
      null,
      null,
      null
    ],
    [
      144,
      154,
      null,
      null,
      null,
      null
    ],
    [
      145,
      155,
      null,
      null,
      null,
      null
    ],
    [
      146,
      156,
      null,
      null,
      null,
      null
    ],
    [
      147,
      157,
      null,
      null,
      null,
      null
    ],
    [
      148,
      null,
      null,
      null,
      null,
      null
    ],
    [
      149,
      null,
      null,
      null,
      null,
      null
    ],
    [
      150,
      null,
      null,
      null,
      null,
      null
    ],
    [
      152,
      null,
      null,
      null,
      null,
      null
    ]
  ],
  "1": [
    [
      1,
      17,
      31,
      52,
      64,
      null
    ],
    [
      2,
      18,
      32,
      53,
      65,
      null
    ],
    [
      3,
      19,
      33,
      56,
      66,
      null
    ],
    [
      4,
      20,
      34,
      55,
      67,
      null
    ],
    [
      5,
      21,
      35,
      54,
      null,
      null
    ],
    [
      6,
      22,
      36,
      58,
      null,
      null
    ],
    [
      7,
      23,
      37,
      59,
      null,
      null
    ],
    [
      8,
      24,
      38,
      57,
      null,
      null
    ],
    [
      9,
      25,
      39,
      60,
      null,
      null
    ],
    [
      10,
      26,
      40,
      61,
      null,
      null
    ],
    [
      11,
      27,
      41,
      62,
      null,
      null
    ],
    [
      29,
      28,
      45,
      63,
      null,
      null
    ],
    [
      30,
      null,
      43,
      null,
      null,
      null
    ],
    [
      null,
      null,
      44,
      null,
      null,
      null
    ],
    [
      null,
      null,
      42,
      null,
      null,
      null
    ]
  ],
  "2": [
    [
      89,
      94,
      101,
      105,
      null,
      null
    ],
    [
      90,
      98,
      102,
      106,
      null,
      null
    ],
    [
      91,
      99,
      103,
      107,
      null,
      null
    ],
    [
      92,
      100,
      104,
      108,
      null,
      null
    ],
    [
      93,
      null,
      null,
      109,
      null,
      null
    ],
    [
      95,
      null,
      null,
      null,
      null,
      null
    ],
    [
      96,
      null,
      null,
      null,
      null,
      null
    ],
    [
      97,
      null,
      null,
      null,
      null,
      null
    ]
  ],
  "5": [
    [
      158,
      169,
      null,
      null,
      null,
      null
    ],
    [
      159,
      170,
      null,
      null,
      null,
      null
    ],
    [
      160,
      171,
      null,
      null,
      null,
      null
    ],
    [
      161,
      172,
      null,
      null,
      null,
      null
    ],
    [
      162,
      173,
      null,
      null,
      null,
      null
    ],
    [
      163,
      174,
      null,
      null,
      null,
      null
    ],
    [
      164,
      175,
      null,
      null,
      null,
      null
    ],
    [
      165,
      176,
      null,
      null,
      null,
      null
    ],
    [
      166,
      177,
      null,
      null,
      null,
      null
    ],
    [
      167,
      178,
      null,
      null,
      null,
      null
    ],
    [
      168,
      179,
      null,
      null,
      null,
      null
    ],
    [
      181,
      180,
      null,
      null,
      null,
      null
    ]
  ]
};
