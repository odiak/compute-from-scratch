/* Observer-only reference. Build as freestanding AArch64. */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef unsigned long u64;
#define R(off) (*(volatile u32 *)(mmio + (off)))
#define BARRIER() __asm__ volatile("dmb sy" ::: "memory")
#define INLINE static inline __attribute__((always_inline))
struct desc { u64 addr; u32 len; u16 flags, next; };
struct queue {
    struct desc desc[8];
    u16 flags, idx, ring[8];
    u32 used[18];
};
INLINE void setup(u64 mmio, unsigned index, volatile struct queue *q) {
    R(0x30) = index;
    R(0x38) = 8;
    R(0x80) = (u32)(u64)q->desc;
    R(0x90) = (u32)(u64)&q->flags;
    R(0xa0) = (u32)(u64)q->used;
    R(0x44) = 1;
}
INLINE void emit(u8 c) {
    while (*(volatile u32 *)0x09000018 & 32) {}
    *(volatile u32 *)0x09000000 = c;
}
INLINE void digit(u8 n) { emit(n < 10 ? '0' + n : 'a' + n - 10); }

void start(void) {
    u64 mmio = 0x0a000000;
    while (R(8) != 1 && mmio < 0x0a004000) mmio += 0x200;
    if (mmio == 0x0a004000) for (;;) {}
    volatile struct queue *rx = (void *)0x40300000, *tx = (void *)0x40301000;
    volatile u8 *in = (void *)0x40302000, *out = (void *)0x40303000;
    R(0x70) = 0;
    R(0x70) = 1;
    R(0x70) = 3;
    R(0x24) = 0;
    R(0x20) = 0;
    R(0x24) = 1;
    R(0x20) = 1;
    R(0x70) = 11;
    setup(mmio, 0, rx);
    setup(mmio, 1, tx);
    rx->desc[0].addr = (u64)in; rx->desc[0].len = 2048; rx->desc[0].flags = 2;
    rx->idx = 1;
    R(0x70) = 15;
    R(0x50) = 0;
    /* Twelve-byte modern virtio header followed by Ethernet and ARP. */
    for (unsigned i = 12; i < 18; ++i) out[i] = 255;
    out[18] = 0x52; out[19] = 0x54; out[21] = 0x12;
    out[22] = 0x34; out[23] = 0x56;
    out[24] = 8; out[25] = 6;
    out[27] = 1; out[28] = 8; out[30] = 6; out[31] = 4; out[33] = 1;
    for (unsigned i = 0; i < 6; ++i) out[34+i] = out[18+i];
    out[40] = 10; out[42] = 2; out[43] = 15;
    out[50] = 10; out[52] = 2; out[53] = 2;
    tx->desc[0].addr = (u64)out; tx->desc[0].len = 54;
    BARRIER();
    tx->idx = 1;
    BARRIER();
    R(0x50) = 1;
    while (!(rx->used[0] >> 16)) {}
    BARRIER();
    for (unsigned i = 34; i < 40; ++i) {
        u8 b = in[i];
        digit(b >> 4); digit(b & 15);
        emit(i == 39 ? '\n' : ':');
    }
    for (;;) {}
}
