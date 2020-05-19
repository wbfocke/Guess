#!/usr/bin/env python

import sys
import sqlite3

import strings


def getAns():
    while True:
        ans = sys.stdin.readline()[0]
        if ans == 'y':
            return True
        elif ans == 'n':
            return False
        else:
            print 'Invalid input, try again. Tard.'
    return


def main():
    notDone = True
    while notDone:
        once()
        print 'Again? (y/n)'
        notDone = getAns()
        continue
    return


def once():

    conn = sqlite3.connect(strings.dbFile)
    cur = conn.cursor()
    
    print strings.intro

    done = False
    #    conn.execute('''
    #select node.node
    #from 
    #    node 
    #    left join node as nodeyes on nodeyes.nodeyes = node.node
    #    left join node as nodeno on nodeno.nodeno = node.node
    #where 
    #    nodeyes.node is null and nodeno.node is null
    #''')
    node = cur.execute('''select node from node order by node asc limit 1;''').fetchone()[0]
    while not done:
        cur.execute('select * from node where node = ?', (node,))
        flurf =  cur.fetchone()
        #print flurf
        (junk, yes, no, text) = flurf
        if yes is None: # leaf
            done = True
            print strings.leafPre, text, strings.leafPost
            resp = getAns()
            if resp:
                print strings.iWin
            else:
                print strings.loseLeaf
                newLeafText = sys.stdin.readline().strip()
                cur.execute('insert into node values (null, null, null, ?);', (newLeafText,))
                newLeafNode = cur.execute('select last_insert_rowid();').fetchone()[0]
                newPath = path and 'nodeyes' or 'nodeno'
                cur.execute("update node set %s = null where node = ?;" % (newPath,), (oldNode,))
                print strings.loseText % (newLeafText, text)
                newInternalText = sys.stdin.readline().strip()
                cur.execute("insert into node values (null, ?, ?, ?);", (newLeafNode, node, newInternalText))
                newInternalNode = cur.execute('select last_insert_rowid();').fetchone()[0]
                cur.execute("update node set %s = ? where node = ?;"% (newPath,), (newInternalNode, oldNode))
                #print cur.execute("select * from node;").fetchall()
                conn.commit()
            pass
        else: # internal
            oldNode = node
            print text, '(y/n)'
            path = getAns()
            node = path and yes or no
            pass
        continue
    
    return


def init():
    conn = sqlite3.connect(strings.dbFile)
    cur = conn.corsor()
    for line in open(strings.setupFile):
        print line
        cur.execute(line)
        continue
    conn.commit()
    conn.close
    return


if __name__ == "__main__":
    main()
