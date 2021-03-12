a = ['a','b','c','d','e','f','g']
b = [1,2,3,4,5,6,7]

##counter = 0
##for letter in a:
##    print(str(b[counter])+letter)
##    counter+=1
##    
##print()
##
##for num, letter in map(lambda a,b :[b,a],a,b):
##    print(str(num)+letter)
##
##print()

print('\n'.join([str(num)+letter for num,letter in map(lambda a,b:[b,a],a,b)]))


