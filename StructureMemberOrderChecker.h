#ifndef __STRUCTUREMEMBERORDERCHECKER_H__
#define __STRUCTUREMEMBERORDERCHECKER_H__

#define SMOCHKER_MEMBER_MAX            10
#define SMOCHKER_USE_RECUR             0

#if (SMOCHKER_MEMBER_MAX < 2)
#error "SMOCHKER_MEMBER_MAX must large than 2 !"
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
#else
// #define SMOCHKER_OFFSETOF(_struct, _member) ((SMOCHKER_SIZE_T)((int)(&((_struct *)0)->_member)))
#define SMOCHKER_OFFSETOF(_struct, _member) ((SMOCHKER_SIZE_T)((long long)(&((_struct *)0)->_member)))
#endif  /* offsetof */
#endif  /* SMOCHKER_OFFSETOF */

#define _SMOCHKER_PAIR(_struct, _first, _second) \
    (SMOCHKER_OFFSETOF(_struct, _first) < SMOCHKER_OFFSETOF(_struct, _second))

#ifdef SMOCHKER
#error "SMOCHKER is defined!"
#endif  /* SMOCHKER */

#if SMOCHKER_USE_RECUR

#define _SMOCHKER_NEXT_SELECT(_struct,             \
                              _1, _2, _3, _4, _5,  \
                              _6, _7, _8, _9, _10, \
                              NAME, ...) _SMOCHKER_NEXT##NAME

#define _SMOCHKER_NEXT(_struct, _current, ...)                    \
    _SMOCHKER_NEXT_SELECT(_struct, ##__VA_ARGS__,                 \
                          _RECUR, _RECUR, _RECUR, _RECUR, _RECUR, \
                          _RECUR, _RECUR, _RECUR, _RECUR, _RECUR, \
                          _END)(_struct, _current, ##__VA_ARGS__)

#define _SMOCHKER_NEXT_RECUR(_struct, _current, _next, ...) \
    (_SMOCHKER_PAIR(_struct, _current, _next) && _SMOCHKER_NEXT(_struct, _next, ##__VA_ARGS__))

#define _SMOCHKER_NEXT_END(_struct, _current) 1

#define _SMOCHKER_IMPL _SMOCHKER_NEXT_RECUR

#else

#define _SMOCHKER_CHECK0(_struct) 0

#define _SMOCHKER_CHECK1(_struct, _current) 1

#define _SMOCHKER_CHECK2(_struct, _current, _next, ...) \
    _SMOCHKER_PAIR(_struct, _current, _next)

#define _SMOCHKER_CHECK3(_struct, _current, _next, ...) \
    (_SMOCHKER_PAIR(_struct, _current, _next) && _SMOCHKER_CHECK2(_struct, _next, ##__VA_ARGS__))

#define _SMOCHKER_CHECK4(_struct, _current, _next, ...) \
    (_SMOCHKER_PAIR(_struct, _current, _next) && _SMOCHKER_CHECK3(_struct, _next, ##__VA_ARGS__))

#define _SMOCHKER_CHECK5(_struct, _current, _next, ...) \
    (_SMOCHKER_PAIR(_struct, _current, _next) && _SMOCHKER_CHECK4(_struct, _next, ##__VA_ARGS__))

#define _SMOCHKER_CHECK6(_struct, _current, _next, ...) \
    (_SMOCHKER_PAIR(_struct, _current, _next) && _SMOCHKER_CHECK5(_struct, _next, ##__VA_ARGS__))

#define _SMOCHKER_CHECK7(_struct, _current, _next, ...) \
    (_SMOCHKER_PAIR(_struct, _current, _next) && _SMOCHKER_CHECK6(_struct, _next, ##__VA_ARGS__))

#define _SMOCHKER_CHECK8(_struct, _current, _next, ...) \
    (_SMOCHKER_PAIR(_struct, _current, _next) && _SMOCHKER_CHECK7(_struct, _next, ##__VA_ARGS__))

#define _SMOCHKER_CHECK9(_struct, _current, _next, ...) \
    (_SMOCHKER_PAIR(_struct, _current, _next) && _SMOCHKER_CHECK8(_struct, _next, ##__VA_ARGS__))

#define _SMOCHKER_CHECK10(_struct, _current, _next, ...) \
    (_SMOCHKER_PAIR(_struct, _current, _next) && _SMOCHKER_CHECK9(_struct, _next, ##__VA_ARGS__))

#define _SMOCHKER_NEXT_SELECT(_struct,             \
                              _1, _2, _3, _4, _5,  \
                              _6, _7, _8, _9, _10, \
                              NAME, ...) _SMOCHKER_CHECK##NAME

#define _SMOCHKER_IMPL(_struct, ...) \
    _SMOCHKER_NEXT_SELECT(_struct, ##__VA_ARGS__, \
                          10, 9, 8, 7, 6,         \
                           5, 4, 3, 2, 1,         \
                           0)(_struct, ##__VA_ARGS__)

#endif

#ifdef _Static_assert
#define SMOCHKER_MSG(_struct, msg, ...) \
    _Static_assert(_SMOCHKER_IMPL(_struct, ##__VA_ARGS__), #msg)
#else
#define SMOCHKER_MSG(_struct, msg, ...) \
    typedef int __compile_time_assert_##msg[_SMOCHKER_IMPL(_struct, ##__VA_ARGS__) ? 1 : -1];
#endif  /* _Static_assert */

#define SMOCHKER(_struct, ...) SMOCHKER_MSG(_struct, _struct##_order_is_error, ##__VA_ARGS__)

#endif  // !__STRUCTUREMEMBERORDERCHECKER_H__
