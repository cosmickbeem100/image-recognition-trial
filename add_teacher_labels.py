#!/opt/conda/bin/python
# -*- coding: utf-8 -*-

import sys
import glob
import os
import re

class ErrorHandler:
	WRONG = 1
	
	def exit(self, m):
		print("[FATAL] " + m)
		sys.exit(self.WRONG)

class ArgsParser:
	ARG_DIR = 1
	LENGTH = 2
	
	def __init__(self, args):
		if len(args) != self.LENGTH:
			ErrorHandler().exit("argments are wrong: " + str(args))
		
		self.dir = args[self.ARG_DIR]

class FileCollecter:
	ALL_FILE = "**"
	
	def __init__(self, dir):
		self.files = glob.glob(self.add_wildcard(dir))
		#ErrorHandler().exit("for debug")
		
	def add_wildcard(self, dir):
		# パスにワイルドカードを付与して返す
		path = os.path.join(dir, self.ALL_FILE)
		#print(path)
		return path
	
	def change_name(self, path, label):
		# 対象ファイルが存在しない場合は異常終了
		if not os.path.exists(path):
			ErrorHandler.exit("there is no file: " + path)
		
		# ファイルパスをディレクトリパスとファイル名に分割
		dir, file = os.path.split(path)
		
		# ファイル名にラベルを追加
		file = label + file 
		
		# ファイル名を変更
		os.rename(path, os.path.join(dir, file))

class LabelMatcher:
	TABLE = {
		"橋本奈々未" : "0",
		"生田絵梨花" : "1",
		"西野七瀬" : "2",
		"白石麻衣" : "3",
		"齋藤飛鳥" : "4"}
	SEPARATER = "_"
	NOT_MATCH = ""
	
	def get_label(self, path):
		label = ""
		file = os.path.basename(path)
		
		# 各ラベルのマッチパターンを試して、マッチする場合はラベルを取得する
		for k in self.TABLE.keys():
			label = self.match(k, file)
			if label is not None: return label
		
		# どのラベルにもマッチしなかった場合、エラーメッセージを出して、ファイル名は変更しない
		print("[ERROR] not matched: " + path)
		return self.NOT_MATCH
	
	def match(self, pattern, path):
		# 与えられたマッチングパターンとマッチする場合は、そのラベルを返す
		matched = re.match(pattern, path)
		if matched is None:
			return None
		print("[matched] " + path)
		return self.TABLE[pattern] + self.SEPARATER

class LabelAdditionManager:
	def __init__(self, args):
		# 対象フォルダパスを取得する
		self.ap = ArgsParser(args)
		
		# フォルダ内のすべてのファイルのパスを取得する
		self.fc = FileCollecter(self.ap.dir)
		
		self.lm = LabelMatcher()
	
	def start(self):
		# すべてのファイルにラベルを付与する
		for i in self.fc.files:
			self.add_label(i)
	
	def add_label(self, file):
		print("processing: " + file)
		
		# ファイル名とラベルをマッチさせる
		label = self.lm.get_label(file)
		
		# マッチするラベルをファイル名の先頭に付与した形でファイル名を変更する
		self.fc.change_name(file, label)

def main(args):
	lam = LabelAdditionManager(args)
	lam.start()

if __name__ == "__main__":
	main(sys.argv)