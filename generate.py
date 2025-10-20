import argparse


class GenerateStructureMemberOrderChecker:
    def __init__(self, member_max=10, use_recur=False, error_msg='order_is_error', debug=False, system=32):
        self.DEBUG = debug
        self.SYSTEM = system
        self.configure(member_max, use_recur, error_msg)

    def configure(self, member_max, use_recur, error_msg):
        if member_max < 2:
            raise ValueError('SMOCHKER_MEMBER_MAX must large than 2!')
        self.SMOCHKER_MEMBER_MAX = member_max
        
        self.SMOCHKER_USE_RECUR = use_recur

        if error_msg is not None:
            if ' ' in error_msg:
                raise ValueError('ERROR_MSG can not have a space!')
            self.ERROR_MSG = error_msg
    
    def generate_component_copyright(self):
        copyright = ''
        copyright += f'''/*==================================================
'''
        with open('LICENSE') as f:
            copyright += f.read()
            f.close()
        if copyright[-1] != '\n':
            copyright += '\n'
        copyright += f'''==================================================*/
'''
        return copyright
    
    def generate_component_head(self):
        head = ''
        if self.DEBUG:
            head += f'''/*==================================================
    Head Start
==================================================*/
'''
        head += f'''#ifndef __STRUCTUREMEMBERORDERCHECKER_H__
#define __STRUCTUREMEMBERORDERCHECKER_H__

#define SMOCHKER_MEMBER_MAX            {self.SMOCHKER_MEMBER_MAX}'''
        if self.SMOCHKER_USE_RECUR:
            head += f'''
#define SMOCHKER_USE_RECUR             1'''
        else:
            head += f'''
#define SMOCHKER_USE_RECUR             0'''
        head += f'''

#if (SMOCHKER_MEMBER_MAX < 2)
#error "SMOCHKER_MEMBER_MAX must large than 2!"
#endif

#ifndef SMOCHKER_SIZE_T
#ifdef size_t
typedef size_t SMOCHKER_SIZE_T;
#else
typedef unsigned int SMOCHKER_SIZE_T;
#endif  /* size_t */
#endif  /* SMOCHKER_SIZE_T */

#ifndef SMOCHKER_OFFSETOF
#ifdef offsetof
#define SMOCHKER_OFFSETOF(_struct, _member) ((SMOCHKER_SIZE_T)offsetof(_struct, _member))
#else'''
        if self.SYSTEM == 64:
            head += f'''
#define SMOCHKER_OFFSETOF(_struct, _member) ((SMOCHKER_SIZE_T)((long long)(&((_struct *)0)->_member)))'''
        else:
            head += f'''
#define SMOCHKER_OFFSETOF(_struct, _member) ((SMOCHKER_SIZE_T)((int)(&((_struct *)0)->_member)))'''
        head += f'''
#endif  /* offsetof */
#endif  /* SMOCHKER_OFFSETOF */

#define _SMOCHKER_PAIR(_struct, _first, _second) \
    (SMOCHKER_OFFSETOF(_struct, _first) < SMOCHKER_OFFSETOF(_struct, _second))

#ifdef SMOCHKER
#error "SMOCHKER is defined!"
#endif  /* SMOCHKER */
'''
        if self.DEBUG:
            head += f'''/*==================================================
    Head End
==================================================*/
'''
        return head
    
    def generate_component_tail(self):
        tail = ''
        if self.DEBUG:
            tail += f'''
/*==================================================
    Tail Start
==================================================*/'''
        tail += f'''
#ifdef _Static_assert
#define SMOCHKER_MSG(_struct, msg, ...) \\
    _Static_assert(_SMOCHKER_IMPL(_struct, ##__VA_ARGS__), #msg)
#else
#define SMOCHKER_MSG(_struct, msg, ...) \\
    typedef int __compile_time_assert_##msg[_SMOCHKER_IMPL(_struct, ##__VA_ARGS__) ? 1 : -1];
#endif  /* _Static_assert */

#define SMOCHKER(_struct, ...) SMOCHKER_MSG(_struct, _struct##_##order_is_error, ##__VA_ARGS__)

#endif  // !__STRUCTUREMEMBERORDERCHECKER_H__
'''
        if self.DEBUG:
            tail += f'''/*==================================================
    Tail End
==================================================*/
'''
        return tail

    def generate_component_method_recur(self):
        raise ValueError('not support this function now!')

    def generate_component_method_linera(self):
        method = ''
        if self.DEBUG:
            method += f'''
/*==================================================
    Method Start
==================================================*/'''

        # _SMOCHKER_CHECKn
        method += f'''
#define _SMOCHKER_CHECK0(_struct) 0
#define _SMOCHKER_CHECK1(_struct, _current) 1
#define _SMOCHKER_CHECK2(_struct, _current, _next, ...) _SMOCHKER_PAIR(_struct, _current, _next)'''
        if self.SMOCHKER_MEMBER_MAX > 2:
            for n in range(3, self.SMOCHKER_MEMBER_MAX + 1):
                method += f'''
#define _SMOCHKER_CHECK{n}(_struct, _current, _next, ...) (_SMOCHKER_PAIR(_struct, _current, _next) && _SMOCHKER_CHECK{n-1}(_struct, _next, ##__VA_ARGS__))'''

        # _SMOCHKER_NEXT_SELECT        
        method += f'''

#define _SMOCHKER_NEXT_SELECT(_struct,             \\
                              _1, _2,'''
        if self.SMOCHKER_MEMBER_MAX > 2:
            for n in range(3, self.SMOCHKER_MEMBER_MAX + 1):
                method += f' _{n},'
                if n % 5 == 0:
                    method += f'''  \\
                              '''
                    if n < self.SMOCHKER_MEMBER_MAX:
                        method = method[:-1]
        if self.SMOCHKER_MEMBER_MAX % 5 != 0:
            method += ' '
        method += f'''NAME, ...) _SMOCHKER_CHECK##NAME
'''
        # _SMOCHKER_IMPL
        method += f'''
#define _SMOCHKER_IMPL(_struct, ...) \\
    _SMOCHKER_NEXT_SELECT(_struct, ##__VA_ARGS__, \\
                         '''
        for n in range(self.SMOCHKER_MEMBER_MAX, 0, -1):
            method += f' {n},'
            if (n - 1) % 5 == 0:
                method += f'''         \\
                          '''
                if (n - 1) > 0:
                    method = method[:-1]
        method += f'''0)(_struct, ##__VA_ARGS__)
'''

        if self.DEBUG:
            method += f'''/*==================================================
    Method End
==================================================*/
'''

        return method
    
    def generate(self, file='StructureMemberOrderChecker.h'):
        copyright = self.generate_component_copyright()
        head = self.generate_component_head()
        tail = self.generate_component_tail()
        method = ''

        if self.SMOCHKER_USE_RECUR:
            method = self.generate_component_method_recur()
        else:
            method = self.generate_component_method_linera()

        context = copyright + head + method + tail
        with open(file, 'w') as f:
            f.write(context)
            f.close()
        print(f'generate {file} success!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='生成结构体成员顺序检查器'.encode('utf-8'),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例：
    %(porg)s                                # 使用默认配置(StructureMemberOrderChecker.h, 10, linera, order_is_error, no debug)
    %(porg)s --save=1.h                     # 设置生成的文件名为1.h
    %(porg)s --member-max=10                # 设置结构体成员数目最大为10
    %(porg)s --method=linera or recur       # 设置检查方法为linera或recur
    %(porg)s --error=order_is_error         # 设置报错信息为order_is_error
    %(porg)s --debug=false                  # 设置调试输出为false
    %(porg)s --system=64                    # 设置系统位数为64位
'''.encode('utf-8')
    )
    
    parser.add_argument(
        '--save',
        type=str,
        default='StructureMemberOrderChecker.h',
        help='设置生成的文件名（默认为StructureMemberOrderChecker.h）'.encode('utf-8')
    )

    parser.add_argument(
        '--member-max',
        type=int,
        default=10,
        help='设置结构体成员数目最大值（默认为10）'.encode('utf-8')
    )

    parser.add_argument(
        '--method',
        type=str,
        default='linera',
        help='设置检查方法（默认为linera）'.encode('utf-8')
    )

    parser.add_argument(
        '--error',
        type=str,
        default='order_is_error',
        help='设置报错信息（默认为order_is_error）'.encode('utf-8')
    )

    parser.add_argument(
        '--debug',
        type=str,
        default='false',
        help='设置是否调试输出（默认为false）'.encode('utf-8')
    )

    parser.add_argument(
        '--system',
        type=int,
        default=32,
        help='设置系统位数（默认为32）'.encode('utf-8')
    )

    args = parser.parse_args()
    if args.method not in ['linera', 'recur']:
        raise ValueError('method must be linera or recur!')
    use_recur = True if args.method == 'recur' else False
    debug = True if args.debug.upper() in ['YES', 'Y'] else False

    if args.member_max >= 100:
        print('are you sure?')
        print('if yes, input string: yes, i\'m sure [your member_max]!')
        print('if member_max is 100, you need input: yes, i\'m sure 100!')
        print('and then input an enter')
        commitment = input()
        if commitment != f'yes, i\'m sure {args.member_max}!':
            raise ValueError('your input string is not able!')

    gen = GenerateStructureMemberOrderChecker(member_max=args.member_max, use_recur=use_recur, error_msg=args.error, debug=debug, system=args.system)
    print('generate checker param:')
    print(args)
    gen.generate(args.save)
