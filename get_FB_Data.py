#!/usr/bin/env python
#-*- coding:UTF-8 -*-

""" Parsing Facebook Data to GDF(gephi) File

Written by Jin C. Hung (sportbass805@gmail.com).

@2014-11-27

2014-12-13 using function
"""

import facebook

#Function: get .gdf file 
def getGDF(pageID, dateSince, dateUntil, limitNum):
	
	print "GET GDF START"
	
	for p in pageID:
		
		
		#GET data of fanpage by ID
		user = graph.get_object(p)
		uName = user["name"]
		print "process ",uName
		
		#FQL (https://developers.facebook.com/docs/technical-guides/fql/)
		feeds_query = "feed?since=%s&until=%s&access_token=%s&limit=%s" %(dateSince, dateUntil, access_token, limitNum)
		feeds = graph.get_connections(user["id"], feeds_query)
		
		#Parsing data
		node_data = {} 
		edge_data = {}	
		
		#Get node data from feeds (PO文者)
		for feed_mcnt in range(len(feeds["data"])):	
			
			#Display on screen 
			#member_d1 = feeds["data"][feed_mcnt]["from"]["id"] + "," + feeds["data"][feed_mcnt]["from"]["name"]
			#member_d1 = member_d1.encode("utf-8")			
			#print member_d1	
			
			#Put poster data into dictionaries
			member_f = feeds["data"][feed_mcnt]["from"]["id"] #poster id		
			if node_data.has_key(member_f) == 0:
				node_data[member_f] = feeds["data"][feed_mcnt]["from"]["name"]
			
			#Get node data from like_feeds	(對PO文按讚者)
			likes = graph.get_connections(feeds["data"][feed_mcnt]["id"], "likes")	
			for like_mcnt in range(len(likes["data"])):		
				
				#Display on screen 
				#member_d2 = likes["data"][like_mcnt]["id"] + "," + likes["data"][like_mcnt]["name"]
				#member_d2 = member_d2.encode("utf-8")
				#print member_d2
						
				member_l = likes["data"][like_mcnt]["id"]			
				if node_data.has_key(member_l) == 0:		
					node_data[member_l] = likes["data"][like_mcnt]["name"]
				
				#Get edge data	(PO文者與按讚者的連結次數)	
				edge = "%s, %s" %(likes["data"][like_mcnt]["id"], feeds["data"][feed_mcnt]["from"]["id"])		
				if edge_data.has_key(edge):
					edge_data[edge] = edge_data[edge] + 1
				else:
					edge_data[edge] = 1

		#Output file
		#---gephi GDF Format
		#nodedef>name [DataType], label [DataType]
		#edgedef>node1 [DataType], node2 [DataType], weight [DataType]
		#----	
		fn = "member_%s.gdf" %p		#file name
		m = open(fn,"w")
		
		m.write("nodedef>name VARCHAR, label VARCHAR")
		m.write("\n")
		for ndata in node_data.items():
			node_write = ndata[0] + ", " + ndata[1]
			node_write = str(node_write.encode("utf-8"))
			m.write("%s \n" %node_write)

		m.write("\n")
			
		m.write("edgedef>node1 VARCHAR, node2 VARCHAR, weight INT")
		m.write("\n")
		for edata in edge_data.items():
			edge_write = edata[0] + ", " + str(edata[1])
			edge_write = str(edge_write.encode("utf-8"))
			m.write("%s \n" %edge_write)	
			
		m.close()
	
	print "GET GDF FINISH"
	
#Function: get basic data and statistic of fanpage
def getCount(pageID, dateSince, dateUntil, limitNum):
	
	print "GET COUNT START"
	
	#Output file			
	n = open("ds.txt","w")
	str0 = "粉絲專頁名稱|按讚數|討論數|文章數|總按讚數|總回應數|平均按讚數|平均回應數"
	n.write(str0)
	n.write("\n")
	n.close()
	
	for p in pageID:
		#GET data of fanpage by ID
		user = graph.get_object(p)	
		
		uName = user["name"]					#fanpage Name		(粉絲專頁名稱)
		uLikes = user["likes"]					#Like fanpage count	(按讚數)
		uTalk = user["talking_about_count"]		#is Talking about	(討論數/談論這個的用戶)
		feedCnt = 0
		likeCnt = 0
		cmtCnt	= 0
		
		feeds_query = "feed?since=%s&until=%s&access_token=%s&limit=%s" %(dateSince, dateUntil, access_token, limitNum)
		feeds = graph.get_connections(user["id"], feeds_query)
		
		feedCnt = len(feeds["data"]) 	#Count feeds (文章數)
		
		for feed_mcnt in range(len(feeds["data"])):			
			
			#Count like of feeds (總按讚數)
			likes = graph.get_connections(feeds["data"][feed_mcnt]["id"], "likes")			
			likeCnt = likeCnt + len(likes["data"])
			
			#Count comment of feeds	(總回應數)
			cmts = graph.get_connections(feeds["data"][feed_mcnt]["id"], "comments")
			cmtCnt = cmtCnt + len(cmts["data"])
		
		if feedCnt > 0 :	
			#Avg. like
			likeAvg = float(likeCnt)/float(feedCnt)			
			#Avg. comment	
			cmtAvg = float(cmtCnt)/float(feedCnt)
		else:
			likeAvg = 0
			cmtAvg = 0
			
		#Output file			
		n = open("ds.txt","a")
				
		str1 = "%s| %d| %d| %d| %d| %d| %f| %f " %(uName, uLikes, uTalk, feedCnt, likeCnt, cmtCnt, likeAvg, cmtAvg)	
		print str1
		str1 = str1.encode("utf-8")
		n.write(str1)	
		n.write("\n")	
		
		n.close()
	
	print "GET COUNT FINISH"

#-------main-------
#Define access_token (from Graph API Explorer)
access_token = "CAACEdEose0cBAPZCRjesQYsyYU5ZAK7kZBRWtkwNb7vfMaXmZArRev4nhm9cI4asS9DPFv3VSCkJy41Wq1WMzNhyW0ZBuKaUaU4ZCPxVgeMChaWmXsvZCvSCtcThelCflqJZAlgTrHxhs4AXR41Y2rgqr2CscribSK6ThuMyGEMe3a0Isi5iGzc19Y7Me9ygATHPbEcDk7xkhbD3ZApdyotUI5ILZAtjThZBzcZD"
graph   = facebook.GraphAPI(access_token)

#GET data of fanpage by ID
pID = ('103640919705348','213063155495946','236207719833366','339459366115928','307969115955037','132350033598538','313919540863','357360988443') #粉絲專頁ID(可多個)
dSince = '2015-03-01'						#起始日期
dUntil = '2015-03-07'						#結束日期
lNum = '10000'								#PO文擷取數

#Call getGDF function
#getGDF(pID, dSince, dUntil, lNum)

#Call getCount function
getCount(pID, dSince, dUntil, lNum)



