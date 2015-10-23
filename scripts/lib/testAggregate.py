#!/usr/bin/python

import argparse
import os
import json
import sys

def createDictIfNecessary(parent, key):
  if key not in parent:
    parent[key] = {}

def diffCaseErrors(classname, before, after, result):
  for testname, errors in after.iteritems():
    if testname in before:
      createDictIfNecessary(result['stillBroken'], classname)
      createDictIfNecessary(result['stillBroken'][classname], 'caseErrors')
      result['stillBroken'][classname]['caseErrors'][testname] = errors
    else:
      createDictIfNecessary(result['broken'], classname)
      result['broken'][classname]['caseErrors'] = errors

def diffClassErrors(classname, before, after, result):
  if 'caseErrors' in after:
    if 'caseErrors' in before:
      diffCaseErrors(classname, before['caseErrors'], after['caseErrors'], result)
    else:
      createDictIfNecessary(result['broken'], classname)
      result['broken'][classname]['caseErrors'] = after['caseErrors']
  elif 'caseErrors' in before:
    createDictIfNecessary(result['fixed'], classname)
    result['fixed'][classname]['caseErrors'] = before['caseErrors']

  if 'suiteErrors' in after:
    if 'suiteErrors' in before:
      createDictIfNecessary(result['stillBroken'], classname)
      result['stillBroken'][classname]['suiteErrors'] = after['suiteErrors']
    else:
      createDictIfNecessary(result['broken'], classname)
      result['broken'][classname]['suiteErrors'] = after['suiteErrors']
  elif 'suiteErrors' in before:
    createDictIfNecessary(result['fixed'], classname)
    result['fixed'][classname]['suiteErrors'] = before['suiteErrors']

def diff(before, after):
  result = { 'fixed' : {}, 'broken': {}, 'stillBroken': {}}
  for classname, errors  in after.iteritems():
    if classname not in before:
      result['broken'][classname] = errors
    else:
      diffClassErrors(classname, before[classname], after[classname], result)
  for classname, test in before.iteritems():
    if classname not in after:
      result['fixed'][classname] = test
  return result


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='''
  Utilitiy to diff mvn junit outputs
  ''', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-b", "--before", help="Before pr")
  parser.add_argument("-a", "--after", help="After pr")
  args = parser.parse_args()
  with open(args.before, 'r') as inputFile:
    before = json.load(inputFile)
  with open(args.after, 'r') as inputFile:
    after = json.load(inputFile)
  print(json.dumps(diff(before, after), sort_keys = True, indent = 2))
