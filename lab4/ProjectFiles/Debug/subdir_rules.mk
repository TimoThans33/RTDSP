################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
build-294964705:
	@$(MAKE) --no-print-directory -Onone -f subdir_rules.mk build-294964705-inproc

build-294964705-inproc: ../dsp_bios_.tcf
	@echo 'Building file: "$<"'
	@echo 'Invoking: TConf'
	"C:/ti/bios_5_42_02_10/xdctools/tconf" -b -Dconfig.importPath="C:/ti/bios_5_42_02_10/packages;" "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

dsp_bios_cfg.cmd: build-294964705 ../dsp_bios_.tcf
dsp_bios_cfg.s??: build-294964705
dsp_bios_cfg_c.c: build-294964705
dsp_bios_cfg.h: build-294964705
dsp_bios_cfg.h??: build-294964705
dsp_bios_.cdb: build-294964705

dsp_bios_cfg.obj: ./dsp_bios_cfg.s?? $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: "$<"'
	@echo 'Invoking: C6000 Compiler'
	"C:/ti/ccsv8/tools/compiler/c6000_7.4.23/bin/cl6x" -mv6700 --abi=coffabi -O2 -g --include_path="H:/RTDSPLab/lab4/ProjectFiles" --include_path="C:/ti/ccsv8/C6000/dsk6713/include" --include_path="C:/ti/ccsv8/C6000/csl/include" --include_path="C:/ti/ccsv8/tools/compiler/c6000_7.4.23/include" --include_path="H:/RTDSPLab/lab4/ProjectFiles/Debug" --include_path="C:/ti/bios_5_42_02_10/packages/ti/bios/include" --include_path="C:/ti/bios_5_42_02_10/packages/ti/rtdx/include/c6000" --define=c6713 --define="_DEBUG" --define="CHIP_6713" --diag_wrap=off --display_error_number --diag_warning=225 --preproc_with_compile --preproc_dependency="dsp_bios_cfg.d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

dsp_bios_cfg_c.obj: ./dsp_bios_cfg_c.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: "$<"'
	@echo 'Invoking: C6000 Compiler'
	"C:/ti/ccsv8/tools/compiler/c6000_7.4.23/bin/cl6x" -mv6700 --abi=coffabi -O2 -g --include_path="H:/RTDSPLab/lab4/ProjectFiles" --include_path="C:/ti/ccsv8/C6000/dsk6713/include" --include_path="C:/ti/ccsv8/C6000/csl/include" --include_path="C:/ti/ccsv8/tools/compiler/c6000_7.4.23/include" --include_path="H:/RTDSPLab/lab4/ProjectFiles/Debug" --include_path="C:/ti/bios_5_42_02_10/packages/ti/bios/include" --include_path="C:/ti/bios_5_42_02_10/packages/ti/rtdx/include/c6000" --define=c6713 --define="_DEBUG" --define="CHIP_6713" --diag_wrap=off --display_error_number --diag_warning=225 --preproc_with_compile --preproc_dependency="dsp_bios_cfg_c.d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

intio.obj: ../intio.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: "$<"'
	@echo 'Invoking: C6000 Compiler'
	"C:/ti/ccsv8/tools/compiler/c6000_7.4.23/bin/cl6x" -mv6700 --abi=coffabi -O2 -g --include_path="H:/RTDSPLab/lab4/ProjectFiles" --include_path="C:/ti/ccsv8/C6000/dsk6713/include" --include_path="C:/ti/ccsv8/C6000/csl/include" --include_path="C:/ti/ccsv8/tools/compiler/c6000_7.4.23/include" --include_path="H:/RTDSPLab/lab4/ProjectFiles/Debug" --include_path="C:/ti/bios_5_42_02_10/packages/ti/bios/include" --include_path="C:/ti/bios_5_42_02_10/packages/ti/rtdx/include/c6000" --define=c6713 --define="_DEBUG" --define="CHIP_6713" --diag_wrap=off --display_error_number --diag_warning=225 --preproc_with_compile --preproc_dependency="intio.d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '


