# Minimal PS2SDK build skeleton.
# Requires a configured PS2DEV/PS2SDK environment.

EE_BIN = mmzero_ps2.elf
EE_OBJS = src/main.o src/game.o src/asset_bank.o
EE_INCS = -Iinclude

ifdef PS2SDK
include $(PS2SDK)/samples/Makefile.pref
include $(PS2SDK)/samples/Makefile.eeglobal
else
$(error PS2SDK is not set. Install/configure PS2Dev before native PS2 build.)
endif

%.o: %.c
	$(EE_CC) $(EE_CFLAGS) $(EE_INCS) -c $< -o $@

$(EE_BIN): $(EE_OBJS)
	$(EE_CC) $(EE_CFLAGS) $(EE_INCS) $(EE_OBJS) -o $@ $(EE_LDFLAGS)

clean:
	rm -f $(EE_OBJS) $(EE_BIN) $(EE_BIN:.elf=.irx)
