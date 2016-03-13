from argparse import ArgumentParser

p=ArgumentParser(usage='it is usage tip', description='the first argument')
p.add_argument('--one', default=1, type=int, help='the first argument')
p.add_argument('--two', default=2, type=int, help='the second argument')
p.add_argument('--docs-dir', default='./', help='document directory')

args = p.parse_args()

print args

print args.one
print args.docs_dir
