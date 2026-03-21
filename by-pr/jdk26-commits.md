# JDK 26 Commit 分析报告

> 生成时间: 2026-03-21
> 数据来源: git log
> 总 Commit 数: 3439

---

## 统计概览

### 按组件分布

| 组件 | Commit 数 | 占比 |
|------|-----------|------|
| gc | 745 | 18.9% |
| compiler | 725 | 18.4% |
| core | 694 | 17.6% |
| test | 491 | 12.5% |
| other | 423 | 10.7% |
| security | 234 | 5.9% |
| network | 208 | 5.3% |
| concurrency | 177 | 4.5% |
| build | 153 | 3.9% |
| jfr | 86 | 2.2% |

### 按月份分布

| 月份 | Commit 数 |
|------|-----------|
| 2025-02 | 4 |
| 2025-03 | 1 |
| 2025-04 | 3 |
| 2025-05 | 1 |
| 2025-06 | 387 |
| 2025-07 | 387 |
| 2025-08 | 357 |
| 2025-09 | 491 |
| 2025-10 | 467 |
| 2025-11 | 426 |
| 2025-12 | 381 |
| 2026-01 | 370 |
| 2026-02 | 388 |
| 2026-03 | 273 |

### Top 30 贡献者

| 排名 | 作者 | Commit 数 |
|------|------|-----------|
| 1 | Thomas Schatzl | 130 |
| 2 | Albert Mingkun Yang | 120 |
| 3 | Matthias Baesken | 90 |
| 4 | Phil Race | 79 |
| 5 | Aleksey Shipilev | 76 |
| 6 | Kim Barrett | 69 |
| 7 | Ioi Lam | 68 |
| 8 | Alexey Semenyuk | 67 |
| 9 | SendaoYan | 61 |
| 10 | Francesco Andreuzzi | 60 |
| 11 | Prasanta Sadhukhan | 55 |
| 12 | Jaikiran Pai | 54 |
| 13 | Erik Gahlin | 54 |
| 14 | Chen Liang | 54 |
| 15 | Sergey Bylokhov | 46 |
| 16 | David Holmes | 46 |
| 17 | Emanuel Peter | 46 |
| 18 | Axel Boldt-Christmas | 46 |
| 19 | Brian Burkhalter | 43 |
| 20 | Jan Lahoda | 41 |
| 21 | Volkan Yazici | 41 |
| 22 | Justin Lu | 40 |
| 23 | Joel Sikström | 40 |
| 24 | William Kemper | 39 |
| 25 | Manuel Hässig | 33 |
| 26 | Leonid Mesnik | 32 |
| 27 | Naoto Sato | 31 |
| 28 | Daniel Fuchs | 30 |
| 29 | Mikhail Yankelevich | 29 |
| 30 | Magnus Ihse Bursie | 29 |

---

## 各组件重要 Commit 列表

### GC (745 Commits)

- [JDK-8376186](https://bugs.openjdk.org/browse/JDK-8376186) 8376186: [VectorAPI] Nomenclature change for concrete vector classes (+17809/-17810) Jatin Bhateja
- [JDK-8372978](https://bugs.openjdk.org/browse/JDK-8372978) 8372978: [VectorAPI] Fix incorrect identity values in UMIN/UMAX reduct (+10315/-6432) Eric Fang
- [JDK-8377447](https://bugs.openjdk.org/browse/JDK-8377447) 8377447: [VectorAPI] Assert wrappers to convert float16 (short) value  (+9034/-7289) Jatin Bhateja
- [JDK-8373935](https://bugs.openjdk.org/browse/JDK-8373935) 8373935: Migrate java/lang/invoke tests away from TestNG (+5268/-5479) Chen Liang
- [JDK-8371446](https://bugs.openjdk.org/browse/JDK-8371446) 8371446: VectorAPI: Add unit tests for masks from various long values (+6447/-3933) Xueming Shen
- [JDK-8342382](https://bugs.openjdk.org/browse/JDK-8342382) 8342382: Implement JEP 522: G1 GC: Improve Throughput by Reducing Sync (+3572/-4628) Thomas Schatzl
- [JDK-8365932](https://bugs.openjdk.org/browse/JDK-8365932) 8365932: Implementation of JEP 516: Ahead-of-Time Object Caching with  (+5269/-1645) Erik Österlund
- [JDK-8360707](https://bugs.openjdk.org/browse/JDK-8360707) 8360707: Globally enumerate all blobs, stubs and entries (+3863/-2129) Andrew Dinn
- [JDK-8367014](https://bugs.openjdk.org/browse/JDK-8367014) 8367014: Rename class Atomic to AtomicAccess (+2554/-2552) Kim Barrett
- [JDK-8338977](https://bugs.openjdk.org/browse/JDK-8338977) 8338977: Parallel: Improve heap resizing heuristics (+892/-3855) Albert Mingkun Yang
- [JDK-8365880](https://bugs.openjdk.org/browse/JDK-8365880) 8365880: Shenandoah: Unify memory usage accounting in ShenandoahFreeSe (+2455/-1351) Kelvin Nilsen
- [JDK-8376187](https://bugs.openjdk.org/browse/JDK-8376187) 8376187: [VectorAPI] Define new lane type constants and pass them to i (+1943/-1565) Jatin Bhateja
- [JDK-8325467](https://bugs.openjdk.org/browse/JDK-8325467) 8325467: Support methods with many arguments in C2 (+2599/-566) Daniel Lundén
- [JDK-8358768](https://bugs.openjdk.org/browse/JDK-8358768) 8358768: [vectorapi] Make VectorOperators.SUADD an Associative (+3158/-1) Ian Graves
- [JDK-8369238](https://bugs.openjdk.org/browse/JDK-8369238) 8369238: Allow virtual thread preemption on some common class initiali (+2248/-445) Patricio Chilano Mateo
- [JDK-8362279](https://bugs.openjdk.org/browse/JDK-8362279) 8362279: [vectorapi] VECTOR_OP_SUADD needs reduction support (+2171/-0) Ian Graves
- [JDK-8370774](https://bugs.openjdk.org/browse/JDK-8370774) 8370774: Merge ModRefBarrierSet into CardTableBarrierSet (+698/-1433) Albert Mingkun Yang
- [JDK-8357471](https://bugs.openjdk.org/browse/JDK-8357471) 8357471: GenShen: Share collector reserves between young and old (+1235/-721) Kelvin Nilsen
- [JDK-8362566](https://bugs.openjdk.org/browse/JDK-8362566) 8362566: Use -Xlog:aot+map to print contents of existing AOT cache (+1313/-463) Ioi Lam
- [JDK-8342692](https://bugs.openjdk.org/browse/JDK-8342692) 8342692: C2: long counted loop/long range checks: don't create loop-ne (+1665/-79) Roland Westrelin
- [JDK-8260555](https://bugs.openjdk.org/browse/JDK-8260555) 8260555: Change the default TIMEOUT_FACTOR from 4 to 1 (+810/-850) Leo Korinth
- [JDK-8316694](https://bugs.openjdk.org/browse/JDK-8316694) 8316694: Implement relocation of nmethod within CodeCache (+1591/-64) Chad Rakoczy
- [JDK-8373595](https://bugs.openjdk.org/browse/JDK-8373595) 8373595: A new ObjectMonitorTable implementation (+1034/-413) Fredrik Bredberg
- [JDK-8365190](https://bugs.openjdk.org/browse/JDK-8365190) 8365190: Remove LockingMode related code from share (+140/-1269) Fredrik Bredberg
- [JDK-8374549](https://bugs.openjdk.org/browse/JDK-8374549) 8374549: Extend MetaspaceClosure to cover non-MetaspaceObj types (+860/-513) Ioi Lam
- [JDK-8376756](https://bugs.openjdk.org/browse/JDK-8376756) 8376756: GenShen: Improve encapsulation of generational collection set (+661/-660) William Kemper
- [JDK-8367013](https://bugs.openjdk.org/browse/JDK-8367013) 8367013: Add Atomic<T> to package/replace idiom of volatile var plus A (+1236/-39) Kim Barrett
- [JDK-8369569](https://bugs.openjdk.org/browse/JDK-8369569) 8369569: Rename methods in regmask.hpp to conform with HotSpot coding  (+629/-617) Daniel Lundén
- [JDK-8350550](https://bugs.openjdk.org/browse/JDK-8350550) 8350550: Preload classes from AOT cache during VM bootstrap (+704/-406) Ioi Lam
- [JDK-8156755](https://bugs.openjdk.org/browse/JDK-8156755) 8156755: [TESTBUG] Fix gc/g1/humongousObjects/objectGraphTest/TestObje (+0/-1067) Thomas Schatzl
- [JDK-8377096](https://bugs.openjdk.org/browse/JDK-8377096) 8377096: Refactor AOTMapLogger::OopDataIterator implementations (+541/-496) Ioi Lam
- [JDK-8354650](https://bugs.openjdk.org/browse/JDK-8354650) 8354650: [PPC64] Try to reduce register definitions (+412/-605) David Briemann
- [JDK-8312116](https://bugs.openjdk.org/browse/JDK-8312116) 8312116: GenShen: make instantaneous allocation rate triggers more tim (+901/-110) Kelvin Nilsen
- [JDK-8358735](https://bugs.openjdk.org/browse/JDK-8358735) 8358735: GenShen: block_start() may be incorrect after class unloading (+883/-42) Kelvin Nilsen
- [JDK-8374316](https://bugs.openjdk.org/browse/JDK-8374316) 8374316: Update copyright year to 2025 for hotspot in files where it w (+451/-451) Sergey Bylokhov
- [JDK-8356548](https://bugs.openjdk.org/browse/JDK-8356548) 8356548: Use ClassFile API instead of ASM to transform classes in test (+307/-517) Chen Liang
- [JDK-8350050](https://bugs.openjdk.org/browse/JDK-8350050) 8350050: Shenandoah: Disable and purge allocation pacing support (+7/-786) Y. Srinivas Ramakrishna
- [JDK-8369186](https://bugs.openjdk.org/browse/JDK-8369186) 8369186: HotSpot Style Guide should permit some uses of the C++ Standa (+536/-240) Kim Barrett
- [JDK-8369068](https://bugs.openjdk.org/browse/JDK-8369068) 8369068: GenShen: Generations still aren't reconciled assertion failur (+361/-401) William Kemper
- [JDK-8238687](https://bugs.openjdk.org/browse/JDK-8238687) 8238687: Investigate memory uncommit during young collections in G1 82 (+529/-223) Ivan Walulya
- [JDK-8377396](https://bugs.openjdk.org/browse/JDK-8377396) 8377396: GenShen: Consolidate and simplify in place region promotions (+423/-295) William Kemper
- [JDK-8373392](https://bugs.openjdk.org/browse/JDK-8373392) 8373392: Replace CDS object subgraphs with @AOTSafeClassInitializer (+456/-236) Ioi Lam
- [JDK-8358586](https://bugs.openjdk.org/browse/JDK-8358586) 8358586: ZGC: Combine ZAllocator and ZObjectAllocator (+335/-353) Joel Sikström
- [JDK-8366475](https://bugs.openjdk.org/browse/JDK-8366475) 8366475: Rename MetaspaceShared class to AOTMetaspace (+332/-332) Ioi Lam
- [JDK-8359965](https://bugs.openjdk.org/browse/JDK-8359965) 8359965: Enable paired pushp and popp instruction usage for APX enable (+341/-322) Srinivas Vamsi Parasa
- [JDK-8358821](https://bugs.openjdk.org/browse/JDK-8358821) 8358821: patch_verified_entry causes problems, use nmethod entry barri (+144/-506) Dean Long
- [JDK-8360163](https://bugs.openjdk.org/browse/JDK-8360163) 8360163: Replace hard-coded checks with AOTRuntimeSetup and AOTSafeCla (+421/-170) Chen Liang
- [JDK-8377307](https://bugs.openjdk.org/browse/JDK-8377307) 8377307: Refactor code for AOT cache pointer compression (+344/-235) Ioi Lam
- [JDK-8373945](https://bugs.openjdk.org/browse/JDK-8373945) 8373945: Use WB.fullGC() in ClassUnloader.unloadClass to force GC for  (+324/-215) SendaoYan
- [JDK-8356716](https://bugs.openjdk.org/browse/JDK-8356716) 8356716: ZGC: Cleanup Uncommit Logic (+395/-139) Axel Boldt-Christmas

*... 还有 695 个 Commits*

### COMPILER (725 Commits)

- [JDK-8351159](https://bugs.openjdk.org/browse/JDK-8351159) 8351159: Remaining cleanups in cpu/x86 after 32-bit x86 removal (+16353/-17326) Anton Seoane Ampudia
- [JDK-8373290](https://bugs.openjdk.org/browse/JDK-8373290) 8373290: Update FreeType to 2.14.1 (+7332/-4950) Jayathirth D V
- [JDK-8344942](https://bugs.openjdk.org/browse/JDK-8344942) 8344942: Template-Based Testing Framework (+6722/-0) Emanuel Peter
- [JDK-8324751](https://bugs.openjdk.org/browse/JDK-8324751) 8324751: C2 SuperWord: Aliasing Analysis runtime check (+5810/-249) Emanuel Peter
- [JDK-8353835](https://bugs.openjdk.org/browse/JDK-8353835) 8353835: Implement JEP 500: Prepare to Make Final Mean Final (+5310/-195) Alan Bateman
- [JDK-8354348](https://bugs.openjdk.org/browse/JDK-8354348) 8354348: Enable Extended EVEX to REX2/REX demotion for commutative ope (+2916/-2567) Srinivas Vamsi Parasa
- [JDK-8367531](https://bugs.openjdk.org/browse/JDK-8367531) 8367531: Template Framework: use scopes and tokens instead of misbehav (+3974/-1005) Emanuel Peter
- [JDK-8357551](https://bugs.openjdk.org/browse/JDK-8357551) 8357551: RISC-V: support CMoveF/D vectorization (+3777/-316) Hamlin Li
- [JDK-8359053](https://bugs.openjdk.org/browse/JDK-8359053) 8359053: Implement JEP 504 - Remove the Applet API (+295/-3137) Phil Race
- [JDK-8367982](https://bugs.openjdk.org/browse/JDK-8367982) 8367982: Unify ObjectSynchronizer and LightweightSynchronizer (+1552/-1718) Fredrik Bredberg
- [JDK-8326609](https://bugs.openjdk.org/browse/JDK-8326609) 8326609: New AES implementation with updates specified in FIPS 197 (+1518/-1515) Shawn M Emery
- [JDK-8340093](https://bugs.openjdk.org/browse/JDK-8340093) 8340093: C2 SuperWord: implement cost model (+2884/-94) Emanuel Peter
- [JDK-8315066](https://bugs.openjdk.org/browse/JDK-8315066) 8315066: Add unsigned bounds and known bits to TypeInt/Long (+2239/-563) Quan Anh Mai
- [JDK-8365776](https://bugs.openjdk.org/browse/JDK-8365776) 8365776: Convert JShell tests to use JUnit instead of TestNG (+1555/-1031) Jan Lahoda
- [JDK-8373026](https://bugs.openjdk.org/browse/JDK-8373026) 8373026: C2 SuperWord and Vector API: vector algorithms test and bench (+2379/-0) Emanuel Peter
- [JDK-8348611](https://bugs.openjdk.org/browse/JDK-8348611) 8348611: Eliminate DeferredLintHandler and emit warnings after attribu (+1338/-942) Archie Cobbs
- [JDK-8371259](https://bugs.openjdk.org/browse/JDK-8371259) 8371259: ML-DSA AVX2 and AVX512 intrinsics and improvements (+1572/-703) Volodymyr Paprotski
- [JDK-8364343](https://bugs.openjdk.org/browse/JDK-8364343) 8364343: Virtual Thread transition management needs to be independent  (+1134/-1043) Patricio Chilano Mateo
- [JDK-8355746](https://bugs.openjdk.org/browse/JDK-8355746) 8355746: Start of release updates for JDK 26 8355748: Add SourceVersio (+1814/-90) Nizar Benalla
- [JDK-8337217](https://bugs.openjdk.org/browse/JDK-8337217) 8337217: Port VirtualMemoryTracker to use VMATree (+892/-888) Afshin Zafari
- [JDK-8372980](https://bugs.openjdk.org/browse/JDK-8372980) 8372980: [VectorAPI] AArch64: Add intrinsic support for unsigned min/m (+1358/-418) Eric Fang
- [JDK-8353290](https://bugs.openjdk.org/browse/JDK-8353290) 8353290: C2: Refactor PhaseIdealLoop::is_counted_loop() (+1104/-612) Kangcheng Xu
- [JDK-8354242](https://bugs.openjdk.org/browse/JDK-8354242) 8354242: VectorAPI: combine vector not operation with compare (+1635/-1) erifan
- [JDK-8359412](https://bugs.openjdk.org/browse/JDK-8359412) 8359412: Template-Framework Library: Operations and Expressions (+1611/-0) Emanuel Peter
- [JDK-8317269](https://bugs.openjdk.org/browse/JDK-8317269) 8317269: Store old classes in linked state in AOT cache (+1482/-87) Ioi Lam
- [JDK-8367530](https://bugs.openjdk.org/browse/JDK-8367530) 8367530: The exhaustiveness errors could be improved (+1449/-99) Jan Lahoda
- [JDK-8370794](https://bugs.openjdk.org/browse/JDK-8370794) 8370794: C2 SuperWord: Long/Integer.compareUnsigned return wrong value (+1401/-101) Hamlin Li
- [JDK-8359761](https://bugs.openjdk.org/browse/JDK-8359761) 8359761: JDK 25 RDP1 L10n resource files update (+1103/-382) Alisen Chung
- [JDK-8370890](https://bugs.openjdk.org/browse/JDK-8370890) 8370890: Start of release updates for JDK 27 8370893: Add SourceVersio (+1415/-48) Nizar Benalla
- [JDK-8373119](https://bugs.openjdk.org/browse/JDK-8373119) 8373119: JDK 26 RDP1 L10n resource files update (+982/-435) Damon Nguyen
- [JDK-8359437](https://bugs.openjdk.org/browse/JDK-8359437) 8359437: Make users and test suite not able to set LockingMode flag 83 (+110/-1130) Anton Artemov
- [JDK-8362561](https://bugs.openjdk.org/browse/JDK-8362561) 8362561: Remove diagnostic option AllowArchivingWithJavaAgent (+51/-1156) Ioi Lam
- [JDK-8364973](https://bugs.openjdk.org/browse/JDK-8364973) 8364973: Add JVMTI stress testing mode (+1196/-7) Leonid Mesnik
- [JDK-8343232](https://bugs.openjdk.org/browse/JDK-8343232) 8343232: PKCS#12 KeyStore support for RFC 9879: Use of Password-Based  (+901/-279) Mark Powers
- [JDK-8367499](https://bugs.openjdk.org/browse/JDK-8367499) 8367499: Refactor exhaustiveness computation from Flow into a separate (+608/-541) Jan Lahoda
- [JDK-8367158](https://bugs.openjdk.org/browse/JDK-8367158) 8367158: C2: create better fill and copy benchmarks, taking alignment  (+1148/-0) Emanuel Peter
- [JDK-8358892](https://bugs.openjdk.org/browse/JDK-8358892) 8358892: RISC-V: jvm crash when running dacapo sunflow after JDK-83525 (+1073/-34) Hamlin Li
- [JDK-8356760](https://bugs.openjdk.org/browse/JDK-8356760) 8356760: VectorAPI: Optimize VectorMask.fromLong for all-true/all-fals (+1093/-13) erfang
- [JDK-8352067](https://bugs.openjdk.org/browse/JDK-8352067) 8352067: Remove the NMT treap and replace its uses with the utilities  (+200/-892) Casper Norrbin
- [JDK-8367656](https://bugs.openjdk.org/browse/JDK-8367656) 8367656: Refactor Constantpool's operand array into two (+613/-459) Johan Sjölen
- [JDK-8378166](https://bugs.openjdk.org/browse/JDK-8378166) 8378166: C2 VectorAPI: NBody / particle life demo (+1031/-0) Emanuel Peter
- [JDK-8348868](https://bugs.openjdk.org/browse/JDK-8348868) 8348868: AArch64: Add backend support for SelectFromTwoVector (+973/-26) Bhavana Kilambi
- [JDK-8327963](https://bugs.openjdk.org/browse/JDK-8327963) 8327963: C2: fix construction of memory graph around Initialize node t (+897/-91) Roland Westrelin
- [JDK-8268850](https://bugs.openjdk.org/browse/JDK-8268850) 8268850: AST model for 'var' variables should more closely adhere to t (+873/-113) Jan Lahoda
- [JDK-8367341](https://bugs.openjdk.org/browse/JDK-8367341) 8367341: C2: apply KnownBits and unsigned bounds to And / Or operation (+651/-334) Quan Anh Mai
- [JDK-8371955](https://bugs.openjdk.org/browse/JDK-8371955) 8371955: Support AVX10 floating point comparison instructions (+771/-199) Mohamed Issa
- [JDK-8366461](https://bugs.openjdk.org/browse/JDK-8366461) 8366461: Remove obsolete method handle invoke logic (+74/-877) Dean Long
- [JDK-8347273](https://bugs.openjdk.org/browse/JDK-8347273) 8347273: C2: VerifyIterativeGVN for Ideal and Identity (+925/-25) Emanuel Peter
- [JDK-8342095](https://bugs.openjdk.org/browse/JDK-8342095) 8342095: Add autovectorizer support for subword vector casts (+782/-106) Jasmine Karthikeyan
- [JDK-8347555](https://bugs.openjdk.org/browse/JDK-8347555) 8347555: [REDO] C2: implement optimization for series of Add of unique (+875/-1) Kangcheng Xu

*... 还有 675 个 Commits*

### NETWORK (208 Commits)

- [JDK-8349910](https://bugs.openjdk.org/browse/JDK-8349910) 8349910: Implement JEP 517: HTTP/3 for the HTTP Client API (+104307/-2639) Daniel Fuchs
- [JDK-8378344](https://bugs.openjdk.org/browse/JDK-8378344) 8378344: Refactor test/jdk/java/net/httpclient/*.java TestNG tests to  (+2814/-2627) Daniel Fuchs
- [JDK-8353738](https://bugs.openjdk.org/browse/JDK-8353738) 8353738: Update TLS unit tests to not use certificates with MD5 signat (+524/-3079) Matthew Donovan
- [JDK-8359956](https://bugs.openjdk.org/browse/JDK-8359956) 8359956: Support algorithm constraints and certificate checks in SunX5 (+1854/-740) Artur Barashev
- [JDK-8360564](https://bugs.openjdk.org/browse/JDK-8360564) 8360564: Implement JEP 524: PEM Encodings of Cryptographic Objects (Se (+1382/-813) Anthony Scarpino
- [JDK-8044609](https://bugs.openjdk.org/browse/JDK-8044609) 8044609: javax.net.debug options not working and documented as expecte (+1257/-860) Sean Coffey
- [JDK-8378163](https://bugs.openjdk.org/browse/JDK-8378163) 8378163: test/jdk/java/net/httpclient/*.java: convert tests that use I (+986/-1005) Daniel Fuchs
- [JDK-8314323](https://bugs.openjdk.org/browse/JDK-8314323) 8314323: Implement JEP 527: TLS 1.3 Hybrid Key Exchange (+1839/-120) Hai-May Chao
- [JDK-8373893](https://bugs.openjdk.org/browse/JDK-8373893) 8373893: Refactor networking http server tests to use JUnit (+940/-899) Michael McMahon
- [JDK-8378111](https://bugs.openjdk.org/browse/JDK-8378111) 8378111: Migrate java/util/jar tests to JUnit (+988/-809) Justin Lu
- [JDK-8367067](https://bugs.openjdk.org/browse/JDK-8367067) 8367067: Improve exception handling in HttpRequest.BodyPublishers (+1665/-67) Volkan Yazici
- [JDK-8372004](https://bugs.openjdk.org/browse/JDK-8372004) 8372004: Have SSLLogger implement System.Logger (+798/-797) Sean Coffey
- [JDK-8374170](https://bugs.openjdk.org/browse/JDK-8374170) 8374170: I/O Poller updates (+1005/-473) Alan Bateman
- [JDK-8372746](https://bugs.openjdk.org/browse/JDK-8372746) 8372746: Some httpserver files could benefit from some formatting clea (+729/-730) Daisuke Yamazaki
- [JDK-8378276](https://bugs.openjdk.org/browse/JDK-8378276) 8378276: Refactor test/jdk/java/net/httpclient/quic/ TestNG tests to J (+678/-724) Daniel Fuchs
- [JDK-8377675](https://bugs.openjdk.org/browse/JDK-8377675) 8377675: java.net.http tests should not depend on ../../../com/sun/net (+602/-800) Daniel Fuchs
- [JDK-8351594](https://bugs.openjdk.org/browse/JDK-8351594) 8351594: JFR: Rate-limited sampling of Java events (+1120/-238) Erik Gahlin
- [JDK-8373515](https://bugs.openjdk.org/browse/JDK-8373515) 8373515: Migrate "test/jdk/java/net/httpclient/" to null-safe "SimpleS (+312/-921) Volkan Yazici
- [JDK-8365072](https://bugs.openjdk.org/browse/JDK-8365072) 8365072: Refactor tests to use PEM API (Phase 2) (+560/-647) Mikhail Yankelevich
- [JDK-8348986](https://bugs.openjdk.org/browse/JDK-8348986) 8348986: Improve coverage of enhanced exception messages (+883/-275) Michael McMahon
- [JDK-8326498](https://bugs.openjdk.org/browse/JDK-8326498) 8326498: java.net.http.HttpClient connection leak using http/2 (+849/-270) Jaikiran Pai
- [JDK-8208693](https://bugs.openjdk.org/browse/JDK-8208693) 8208693: HttpClient: Extend the request timeout's scope to cover the r (+1088/-25) Volkan Yazici
- [JDK-8371475](https://bugs.openjdk.org/browse/JDK-8371475) 8371475: HttpClient: Implement CUBIC congestion controller (+764/-262) Daniel Jeliński
- [JDK-8378565](https://bugs.openjdk.org/browse/JDK-8378565) 8378565: Refactor test/jdk/java/net/httpclient/http3/*.java TestNG tes (+505/-490) Daniel Fuchs
- [JDK-8369595](https://bugs.openjdk.org/browse/JDK-8369595) 8369595: HttpClient: HttpHeaders.firstValueAsLong failures should be c (+546/-423) Volkan Yazici
- [JDK-8329829](https://bugs.openjdk.org/browse/JDK-8329829) 8329829: HttpClient: Add a BodyPublishers.ofFileChannel method (+849/-5) Volkan Yazici
- [JDK-8373808](https://bugs.openjdk.org/browse/JDK-8373808) 8373808: Refactor java/net/httpclient qpack and hpack tests to use JUn (+427/-398) Aleksei Efimov
- [JDK-8325766](https://bugs.openjdk.org/browse/JDK-8325766) 8325766: Extend CertificateBuilder to create trust and end entity cert (+206/-608) Matthew Donovan
- [JDK-8365069](https://bugs.openjdk.org/browse/JDK-8365069) 8365069: Refactor tests to use PEM API (Phase 1) (+324/-442) Koushik Thirupattur
- [JDK-8366575](https://bugs.openjdk.org/browse/JDK-8366575) 8366575: Remove SDP support (+0/-732) Volkan Yazici
- [JDK-8359223](https://bugs.openjdk.org/browse/JDK-8359223) 8359223: HttpClient: Remove leftovers from the SecurityManager cleanup (+0/-701) Volkan Yazici
- [JDK-8370024](https://bugs.openjdk.org/browse/JDK-8370024) 8370024: HttpClient: QUIC congestion controller doesn't implement paci (+673/-16) Daniel Jeliński
- [JDK-8368528](https://bugs.openjdk.org/browse/JDK-8368528) 8368528: HttpClient.Builder.connectTimeout should accept arbitrarily l (+621/-57) Volkan Yazici
- [JDK-8371802](https://bugs.openjdk.org/browse/JDK-8371802) 8371802: Do not let QUIC connection to idle terminate when HTTP/3 is c (+577/-99) Jaikiran Pai
- [JDK-8378598](https://bugs.openjdk.org/browse/JDK-8378598) 8378598: Refactor tests under test/jdk/java/net/httpclient/websocket f (+333/-310) Daniel Fuchs
- [JDK-8378599](https://bugs.openjdk.org/browse/JDK-8378599) 8378599: Refactor tests under test/jdk/java/net/httpclient/whitebox fr (+323/-303) Daniel Fuchs
- [JDK-8377302](https://bugs.openjdk.org/browse/JDK-8377302) 8377302: HttpServer::stop uses full timeout duration if handler throws (+459/-80) Daniel Fuchs
- [JDK-8376031](https://bugs.openjdk.org/browse/JDK-8376031) 8376031: HttpsURLConnection.getServerCertificates() throws "java.lang. (+416/-96) Daniel Fuchs
- [JDK-8361060](https://bugs.openjdk.org/browse/JDK-8361060) 8361060: Keep track of the origin server against which a jdk.internal. (+416/-89) Jaikiran Pai
- [JDK-8272758](https://bugs.openjdk.org/browse/JDK-8272758) 8272758: Improve HttpServer to avoid partial file name matches while m (+471/-26) Volkan Yazici
- [JDK-8367561](https://bugs.openjdk.org/browse/JDK-8367561) 8367561: Getting some "header" property from a file:// URL causes a fi (+443/-37) Jaikiran Pai
- [JDK-8379477](https://bugs.openjdk.org/browse/JDK-8379477) 8379477: Tests in test/jdk/com/sun/net/httpserver/ may need to use oth (+257/-221) Jaikiran Pai
- [JDK-8332623](https://bugs.openjdk.org/browse/JDK-8332623) 8332623: Remove setTTL()/getTTL() methods from DatagramSocketImpl/Mult (+25/-445) Jaikiran Pai
- [JDK-8358958](https://bugs.openjdk.org/browse/JDK-8358958) 8358958: (aio) AsynchronousByteChannel.read/write should throw IAE if  (+437/-33) Alan Bateman
- [JDK-8378164](https://bugs.openjdk.org/browse/JDK-8378164) 8378164: test/jdk/java/net/httpclient/http3/*.java: convert tests that (+254/-205) Daniel Fuchs
- [JDK-8368493](https://bugs.openjdk.org/browse/JDK-8368493) 8368493: Disable most test JSSE debug output by default, and increase  (+357/-102) Bradford Wetmore
- [JDK-8372198](https://bugs.openjdk.org/browse/JDK-8372198) 8372198: Avoid closing PlainHttpConnection while holding a lock (+422/-25) Daniel Fuchs
- [JDK-8378398](https://bugs.openjdk.org/browse/JDK-8378398) 8378398: Modernize test/jdk/java/net/URLClassLoader/HttpTest.java (+254/-189) Eirik Bjørsnøs
- [JDK-8378879](https://bugs.openjdk.org/browse/JDK-8378879) 8378879: Refactor java/nio/channels/Channels TestNG tests to use JUnit (+229/-195) Brian Burkhalter
- [JDK-8361639](https://bugs.openjdk.org/browse/JDK-8361639) 8361639: JFR: Incorrect top frame for I/O events (+402/-17) Erik Gahlin

*... 还有 158 个 Commits*

### SECURITY (234 Commits)

- [JDK-8374219](https://bugs.openjdk.org/browse/JDK-8374219) 8374219: Fix issues in jpackage's Executor class (+8888/-1907) Alexey Semenyuk
- [JDK-8376038](https://bugs.openjdk.org/browse/JDK-8376038) 8376038: Refactor java/sql tests to use JUnit 8376629: Refactor javax/ (+2513/-2135) Justin Lu
- [JDK-8336695](https://bugs.openjdk.org/browse/JDK-8336695) 8336695: Update Commons BCEL to Version 6.10.0 (+2461/-1128) Joe Wang
- [JDK-8325448](https://bugs.openjdk.org/browse/JDK-8325448) 8325448: Hybrid Public Key Encryption (+2120/-230) Weijun Wang
- [JDK-8379798](https://bugs.openjdk.org/browse/JDK-8379798) 8379798: Refactor remaining tests in javax/xml/jaxp/functional to JUni (+1140/-1130) David Beaumont
- [JDK-8355904](https://bugs.openjdk.org/browse/JDK-8355904) 8355904: Use variadic macros for J2dTrace (+1044/-1083) Nikita Gubarkov
- [JDK-8367859](https://bugs.openjdk.org/browse/JDK-8367859) 8367859: Remove nio exception gensrc (+1529/-526) Magnus Ihse Bursie
- [JDK-8347938](https://bugs.openjdk.org/browse/JDK-8347938) 8347938: Add Support for the Latest ML-KEM and ML-DSA Private Key Enco (+1488/-286) Weijun Wang
- [JDK-8244336](https://bugs.openjdk.org/browse/JDK-8244336) 8244336: Restrict algorithms at JCE layer (+1403/-202) Valerie Peng
- [JDK-8373631](https://bugs.openjdk.org/browse/JDK-8373631) 8373631: Improve classes in the "jdk.jpackage.internal.util.function"  (+1336/-258) Alexey Semenyuk
- [JDK-8358468](https://bugs.openjdk.org/browse/JDK-8358468) 8358468: Enhance code consistency: java.desktop/macos (+1216/-357) Sergey Bylokhov
- [JDK-8371438](https://bugs.openjdk.org/browse/JDK-8371438) 8371438: jpackage should handle the case when "--mac-sign" is specifie (+1394/-134) Alexey Semenyuk
- [JDK-8374310](https://bugs.openjdk.org/browse/JDK-8374310) 8374310: Update copyright year to 2025 for client-libs in files where  (+565/-565) Sergey Bylokhov
- [JDK-8367104](https://bugs.openjdk.org/browse/JDK-8367104) 8367104: Check for RSASSA-PSS parameters when validating certificates  (+744/-166) Artur Barashev
- [JDK-8349732](https://bugs.openjdk.org/browse/JDK-8349732) 8349732: Add support for JARs signed with ML-DSA (+718/-104) Weijun Wang
- [JDK-8379426](https://bugs.openjdk.org/browse/JDK-8379426) 8379426: [macos] jpackage: runtime bundle version suffix is out of syn (+582/-211) Alexey Semenyuk
- [JDK-8268406](https://bugs.openjdk.org/browse/JDK-8268406) 8268406: Deallocate jmethodID native memory (+456/-295) Coleen Phillimore
- [JDK-8356997](https://bugs.openjdk.org/browse/JDK-8356997) 8356997: /etc/krb5.conf parser should not forbid include/includedir di (+487/-108) Weijun Wang
- [JDK-8365820](https://bugs.openjdk.org/browse/JDK-8365820) 8365820: Apply certificate scope constraints to algorithms in "signatu (+536/-53) Artur Barashev
- [JDK-8358171](https://bugs.openjdk.org/browse/JDK-8358171) 8358171: Additional code coverage for PEM API (+533/-43) Fernando Guallini
- [JDK-8378893](https://bugs.openjdk.org/browse/JDK-8378893) 8378893: X25519 should utilize a larger limb size (+535/-35) Shawn Emery
- [JDK-8333857](https://bugs.openjdk.org/browse/JDK-8333857) 8333857: Test sun/security/ssl/SSLSessionImpl/ResumeChecksServer.java  (+261/-297) Anthony Scarpino
- [JDK-8359919](https://bugs.openjdk.org/browse/JDK-8359919) 8359919: Minor java.util.concurrent doc improvements 8187775: AtomicRe (+304/-222) Doug Lea
- [JDK-8361212](https://bugs.openjdk.org/browse/JDK-8361212) 8361212: Remove AffirmTrust root CAs (+12/-507) Rajan Halade
- [JDK-8368032](https://bugs.openjdk.org/browse/JDK-8368032) 8368032: Enhance Certificate Checking (+452/-47) Jamil Nimeh
- [JDK-8367585](https://bugs.openjdk.org/browse/JDK-8367585) 8367585: Prevent creation of unrepresentable Utf8Entry (+327/-170) Chen Liang
- [JDK-8359170](https://bugs.openjdk.org/browse/JDK-8359170) 8359170: Add 2 TLS and 2 CS Sectigo roots (+479/-4) Rajan Halade
- [JDK-8365953](https://bugs.openjdk.org/browse/JDK-8365953) 8365953: Key manager returns no certificates when handshakeSession is  (+436/-44) Artur Barashev
- [JDK-8369995](https://bugs.openjdk.org/browse/JDK-8369995) 8369995: Fix StringIndexOutOfBoundsException and implement extra loggi (+396/-49) Mikhail Yankelevich
- [JDK-8365588](https://bugs.openjdk.org/browse/JDK-8365588) 8365588: defineClass that accepts a ByteBuffer does not work as expect (+432/-5) Xueming Shen
- [JDK-8375480](https://bugs.openjdk.org/browse/JDK-8375480) 8375480: Remove usage of AppContext from javax/swing/text (+36/-381) Phil Race
- [JDK-8352728](https://bugs.openjdk.org/browse/JDK-8352728) 8352728: InternalError loading java.security due to Windows parent fol (+273/-128) Francisco Ferrari Bihurriet
- [JDK-8361526](https://bugs.openjdk.org/browse/JDK-8361526) 8361526: Synchronize ClassFile API verifier with hotspot (+251/-137) Chen Liang
- [JDK-8277489](https://bugs.openjdk.org/browse/JDK-8277489) 8277489: Rewrite JAAS UnixLoginModule with FFM (+220/-165) Weijun Wang
- [JDK-8374808](https://bugs.openjdk.org/browse/JDK-8374808) 8374808: Add new methods to KeyStore and KeyStoreSpi that return the c (+291/-89) Mikhail Yankelevich
- [JDK-8354469](https://bugs.openjdk.org/browse/JDK-8354469) 8354469: Keytool exposes the password in plain text when command is pi (+323/-48) Weijun Wang
- [JDK-8368226](https://bugs.openjdk.org/browse/JDK-8368226) 8368226: Remove Thread.stop (+9/-343) Alan Bateman
- [JDK-8365863](https://bugs.openjdk.org/browse/JDK-8365863) 8365863: /test/jdk/sun/security/pkcs11/Cipher tests skip without Skipp (+187/-156) Mikhail Yankelevich
- [JDK-8379154](https://bugs.openjdk.org/browse/JDK-8379154) 8379154: Refactor Selector TestNG tests to use JUnit (+190/-150) Brian Burkhalter
- [JDK-8353749](https://bugs.openjdk.org/browse/JDK-8353749) 8353749: Improve security warning when using JKS or JCEKS keystores (+319/-21) Hai-May Chao
- [JDK-8362268](https://bugs.openjdk.org/browse/JDK-8362268) 8362268: NPE thrown from SASL GSSAPI impl when  TLS is  used with QOP  (+306/-12) Jaikiran Pai
- [JDK-8372754](https://bugs.openjdk.org/browse/JDK-8372754) 8372754: Add wrapper for <cstdlib> 8369205: AIX build break in forbidd (+193/-98) Kim Barrett
- [JDK-8370885](https://bugs.openjdk.org/browse/JDK-8370885) 8370885: Default namedGroups values are not being filtered against alg (+190/-74) Artur Barashev
- [JDK-8368050](https://bugs.openjdk.org/browse/JDK-8368050) 8368050: Validation missing in ClassFile signature factories (+227/-32) Chen Liang
- [JDK-8369282](https://bugs.openjdk.org/browse/JDK-8369282) 8369282: Distrust TLS server certificates anchored by Chunghwa ePKI Ro (+244/-2) Mark Powers
- [JDK-8337853](https://bugs.openjdk.org/browse/JDK-8337853) 8337853: Remove SunLayoutEngineKey and SunLayoutEngineFactory and its  (+24/-216) Phil Race
- [JDK-8377191](https://bugs.openjdk.org/browse/JDK-8377191) 8377191: Remove AppContext from KeyboardFocusManager (+46/-187) Phil Race
- [JDK-8368984](https://bugs.openjdk.org/browse/JDK-8368984) 8368984: Extra slashes in Cipher transformation leads to NSPE instead  (+111/-119) Valerie Peng
- [JDK-8350689](https://bugs.openjdk.org/browse/JDK-8350689) 8350689: Turn on timestamp and thread metadata by default for java.sec (+54/-169) Sean Coffey
- [JDK-8367994](https://bugs.openjdk.org/browse/JDK-8367994) 8367994: test/jdk/sun/security/pkcs11/Signature/ tests pass when they  (+160/-60) Mikhail Yankelevich

*... 还有 184 个 Commits*

### CORE (694 Commits)

- [JDK-8354548](https://bugs.openjdk.org/browse/JDK-8354548) 8354548: Update CLDR to Version 48.0 (+120372/-41544) Naoto Sato
- [JDK-8333727](https://bugs.openjdk.org/browse/JDK-8333727) 8333727: Use JOpt in jpackage to parse command line 8371384: libapplau (+18471/-6636) Alexey Semenyuk
- [JDK-8373830](https://bugs.openjdk.org/browse/JDK-8373830) 8373830: Refactor test/jdk/java/time/test tests to use JUnit over Test (+13033/-11460) Justin Lu
- [JDK-8375057](https://bugs.openjdk.org/browse/JDK-8375057) 8375057: Update HarfBuzz to 12.3.2 (+11830/-9727) Damon Nguyen
- [JDK-8366178](https://bugs.openjdk.org/browse/JDK-8366178) 8366178: Implement JEP 526: Lazy Constants (Second Preview) 8371882: I (+2784/-3536) Per Minborg
- [JDK-8346944](https://bugs.openjdk.org/browse/JDK-8346944) 8346944: Update Unicode Data Files to 17.0.0 8346947: Update ICU4J to  (+2327/-1632) Naoto Sato
- [JDK-8368030](https://bugs.openjdk.org/browse/JDK-8368030) 8368030: Make package bundlers stateless (+2414/-1498) Alexey Semenyuk
- [JDK-8366017](https://bugs.openjdk.org/browse/JDK-8366017) 8366017: Extend the set of inputs handled by fast paths in FloatingDec (+1589/-2199) Raffaello Giulietti
- [JDK-8369432](https://bugs.openjdk.org/browse/JDK-8369432) 8369432: Add Support for JDBC 4.5 MR (+2460/-357) Lance Andersen
- [JDK-8358540](https://bugs.openjdk.org/browse/JDK-8358540) 8358540: Enhance MathUtils in view of FloatingDecimal enhancements (+1300/-1438) Raffaello Giulietti
- [JDK-8365555](https://bugs.openjdk.org/browse/JDK-8365555) 8365555: Cleanup redundancies in jpackage implementation (+2107/-415) Alexey Semenyuk
- [JDK-8378631](https://bugs.openjdk.org/browse/JDK-8378631) 8378631: Update Zlib Data Compression Library to Version 1.3.2 (+1442/-1015) Jaikiran Pai
- [JDK-8370122](https://bugs.openjdk.org/browse/JDK-8370122) 8370122: jpackage test lib improvements (+2285/-96) Alexey Semenyuk
- [JDK-8375063](https://bugs.openjdk.org/browse/JDK-8375063) 8375063: Update Libpng to 1.6.54 (+1399/-963) Jayathirth D V
- [JDK-8358666](https://bugs.openjdk.org/browse/JDK-8358666) 8358666: [REDO] Implement JEP 509: JFR CPU-Time Profiling (+2191/-140) Johannes Bechberger
- [JDK-8358628](https://bugs.openjdk.org/browse/JDK-8358628) 8358628: [BACKOUT] 8342818: Implement JEP 509: JFR CPU-Time Profiling (+140/-2178) Markus Grönlund
- [JDK-8342818](https://bugs.openjdk.org/browse/JDK-8342818) 8342818: Implement JEP 509: JFR CPU-Time Profiling (+2178/-140) Johannes Bechberger
- [JDK-8375323](https://bugs.openjdk.org/browse/JDK-8375323) 8375323: Improve handling of the "--app-content" and "--input" options (+1706/-579) Alexey Semenyuk
- [JDK-8366455](https://bugs.openjdk.org/browse/JDK-8366455) 8366455: Move VarHandles.GuardMethodGenerator to execute on build (+340/-1857) Chen Liang
- [JDK-8360459](https://bugs.openjdk.org/browse/JDK-8360459) 8360459: UNICODE_CASE and character class with non-ASCII range does no (+2084/-5) Xueming Shen
- [JDK-8377509](https://bugs.openjdk.org/browse/JDK-8377509) 8377509: Add licenses for gcc 14.2.0 (+2084/-0) Jesper Wilhelmsson
- [JDK-8365606](https://bugs.openjdk.org/browse/JDK-8365606) 8365606: Container code should not be using jlong/julong (+1202/-794) Severin Gehwolf
- [JDK-8356870](https://bugs.openjdk.org/browse/JDK-8356870) 8356870: HotSpotDiagnosticMXBean.dumpThreads and jcmd Thread.dump_to_f (+1547/-421) Alan Bateman
- [JDK-8357404](https://bugs.openjdk.org/browse/JDK-8357404) 8357404: jpackage should attempt to get a package version from the JDK (+1563/-142) Alexey Semenyuk
- [JDK-8351194](https://bugs.openjdk.org/browse/JDK-8351194) 8351194: Clean up Hotspot SA after 32-bit x86 removal (+84/-1578) Kerem Kat
- [JDK-8366837](https://bugs.openjdk.org/browse/JDK-8366837) 8366837: Clean up gensrc by spp.Spp (+759/-798) Magnus Ihse Bursie
- [JDK-8365400](https://bugs.openjdk.org/browse/JDK-8365400) 8365400: Enhance JFR to emit file and module metadata for class loadin (+1210/-337) Markus Grönlund
- [JDK-8360037](https://bugs.openjdk.org/browse/JDK-8360037) 8360037: Refactor ImageReader in preparation for Valhalla support (+870/-616) David Beaumont
- [JDK-8365675](https://bugs.openjdk.org/browse/JDK-8365675) 8365675: Add String Unicode Case-Folding Support (+1245/-212) Xueming Shen
- [JDK-8368877](https://bugs.openjdk.org/browse/JDK-8368877) 8368877: Generate Jextract bindings for Kqueue (+1343/-0) Darragh Clarke
- [JDK-8314488](https://bugs.openjdk.org/browse/JDK-8314488) 8314488: Compiling the JDK with C++17 (+1151/-88) Kim Barrett
- [JDK-8376277](https://bugs.openjdk.org/browse/JDK-8376277) 8376277: Migrate java/lang/reflect tests away from TestNG (+513/-708) Chen Liang
- [JDK-8379158](https://bugs.openjdk.org/browse/JDK-8379158) 8379158: Update FreeType to 2.14.2 (+400/-810) Jayathirth D V
- [JDK-8379155](https://bugs.openjdk.org/browse/JDK-8379155) 8379155: Refactor Files TestNG tests to use JUnit (+591/-577) Brian Burkhalter
- [JDK-8358734](https://bugs.openjdk.org/browse/JDK-8358734) 8358734: Remove JavaTimeSupplementary resource bundles (+301/-830) Naoto Sato
- [JDK-8358731](https://bugs.openjdk.org/browse/JDK-8358731) 8358731: Remove jdk.internal.access.JavaAWTAccess.java (+0/-1110) Phil Race
- [JDK-8367857](https://bugs.openjdk.org/browse/JDK-8367857) 8367857: Implement JEP 525: Structured Concurrency (Sixth Preview) (+784/-313) Alan Bateman
- [JDK-8369590](https://bugs.openjdk.org/browse/JDK-8369590) 8369590: LocaleEnhanceTest has incorrectly passing test case (+485/-598) Justin Lu
- [JDK-8366691](https://bugs.openjdk.org/browse/JDK-8366691) 8366691: JShell should support a more convenient completion (+881/-162) Jan Lahoda
- [JDK-8366678](https://bugs.openjdk.org/browse/JDK-8366678) 8366678: Use JUnit in test/langtools/tools/javac (+556/-458) Christian Stein
- [JDK-8361635](https://bugs.openjdk.org/browse/JDK-8361635) 8361635: Missing List length validation in the Class-File API (+866/-111) Chen Liang
- [JDK-8352075](https://bugs.openjdk.org/browse/JDK-8352075) 8352075: Perf regression accessing fields (+904/-70) Radim Vansa
- [JDK-8364361](https://bugs.openjdk.org/browse/JDK-8364361) 8364361: [process] java.lang.Process should implement Closeable (+945/-6) Roger Riggs
- [JDK-8376234](https://bugs.openjdk.org/browse/JDK-8376234) 8376234: Migrate java/lang/constant tests away from TestNG (+372/-550) Chen Liang
- [JDK-8377514](https://bugs.openjdk.org/browse/JDK-8377514) 8377514: jpackage: support passing multiple exceptions to the top-leve (+635/-271) Alexey Semenyuk
- [JDK-8346719](https://bugs.openjdk.org/browse/JDK-8346719) 8346719: Add relaunchers to the static JDK image for missing executabl (+678/-190) Magnus Ihse Bursie
- [JDK-8378298](https://bugs.openjdk.org/browse/JDK-8378298) 8378298: Remove obsolete CDS string tests (+12/-841) Ioi Lam
- [JDK-8379441](https://bugs.openjdk.org/browse/JDK-8379441) 8379441: Refactor jaxp/javax catalog tests to use JUnit (+412/-436) David Beaumont
- [JDK-8361614](https://bugs.openjdk.org/browse/JDK-8361614) 8361614: Missing sub-int value validation in the Class-File API (+636/-191) Chen Liang
- [JDK-8362598](https://bugs.openjdk.org/browse/JDK-8362598) 8362598: [macos] Add tests for custom info plist files (+739/-81) Alexander Matveev

*... 还有 644 个 Commits*

### CONCURRENCY (177 Commits)

- [JDK-8377797](https://bugs.openjdk.org/browse/JDK-8377797) 8377797: Remove SA support for MethodData and the printmdo command (+12/-2445) Coleen Phillimore
- [JDK-8372188](https://bugs.openjdk.org/browse/JDK-8372188) 8372188: AArch64: Generate atomic match rules from M4 stencils (+1156/-1193) Aleksey Shipilev
- [JDK-8307495](https://bugs.openjdk.org/browse/JDK-8307495) 8307495: Specialize atomic bitset functions for aix-ppc (+749/-890) David Briemann
- [JDK-8364258](https://bugs.openjdk.org/browse/JDK-8364258) 8364258: ThreadGroup constant pool serialization is not normalized (+420/-471) Markus Grönlund
- [JDK-8342730](https://bugs.openjdk.org/browse/JDK-8342730) 8342730: Get rid of SummaryDiff in VMATree (+364/-268) Afshin Zafari
- [JDK-8377909](https://bugs.openjdk.org/browse/JDK-8377909) 8377909: Replace SummaryDiff's array implementation with a hashtable (+359/-178) Johan Sjölen
- [JDK-8377996](https://bugs.openjdk.org/browse/JDK-8377996) 8377996: [REDO] NMT: Consolidate [Virtual/Committed/Reserved]Regions i (+239/-293) Afshin Zafari
- [JDK-8377997](https://bugs.openjdk.org/browse/JDK-8377997) 8377997: [BACKOUT] 8366241: NMT: Consolidate [Virtual/Committed/Reserv (+293/-239) Afshin Zafari
- [JDK-8366241](https://bugs.openjdk.org/browse/JDK-8366241) 8366241: NMT: Consolidate [Virtual/Committed/Reserved]Regions into one (+239/-293) Afshin Zafari
- [JDK-8367332](https://bugs.openjdk.org/browse/JDK-8367332) 8367332: Replace BlockTree tree logic with an intrusive red-black tree (+94/-350) Casper Norrbin
- [JDK-8265754](https://bugs.openjdk.org/browse/JDK-8265754) 8265754: Move suspend/resume API from HandshakeState (+241/-159) Anton Artemov
- [JDK-8366082](https://bugs.openjdk.org/browse/JDK-8366082) 8366082: Improve queue size computation in CPU-time sampler (+292/-23) Johannes Bechberger
- [JDK-8373366](https://bugs.openjdk.org/browse/JDK-8373366) 8373366: HandshakeState should disallow suspend ops for disabler threa (+286/-20) Serguei Spitsyn
- [JDK-8369505](https://bugs.openjdk.org/browse/JDK-8369505) 8369505: jhsdb jstack cannot handle continuation stub (+297/-4) Yasumasa Suenaga
- [JDK-8319589](https://bugs.openjdk.org/browse/JDK-8319589) 8319589: Attach from root to a user java process not supported in Mac (+252/-42) Sergey Chernyshev
- [JDK-8372528](https://bugs.openjdk.org/browse/JDK-8372528) 8372528: Unify atomic exchange and compare exchange (+137/-147) Axel Boldt-Christmas
- [JDK-8282441](https://bugs.openjdk.org/browse/JDK-8282441) 8282441: [LOOM] The debug agent should attempt to free vthread ThreadN (+205/-57) Chris Plummer
- [JDK-8377128](https://bugs.openjdk.org/browse/JDK-8377128) 8377128: Add missing @Override annotations in "java.beans.*" packages (+219/-26) Sergey Bylokhov
- [JDK-8225354](https://bugs.openjdk.org/browse/JDK-8225354) 8225354: serviceability/jvmti/ModuleAwareAgents/ThreadStart failed wit (+0/-230) Serguei Spitsyn
- [JDK-8361067](https://bugs.openjdk.org/browse/JDK-8361067) 8361067: Test ExtraButtonDrag.java requires frame.dispose in finally b (+124/-88) Ravi Gupta
- [JDK-8358429](https://bugs.openjdk.org/browse/JDK-8358429) 8358429: JFR: minimize the time the Threads_lock is held for sampling (+146/-63) Markus Grönlund
- [JDK-8360048](https://bugs.openjdk.org/browse/JDK-8360048) 8360048: NMT crash in gtest/NMTGtests.java: fatal error: NMT corruptio (+104/-103) Afshin Zafari
- [JDK-8367719](https://bugs.openjdk.org/browse/JDK-8367719) 8367719: Refactor JNI code that uses class_to_verify_considering_redef (+93/-110) Ioi Lam
- [JDK-8369211](https://bugs.openjdk.org/browse/JDK-8369211) 8369211: AArch64: Devirtualize class RelocActions (+81/-120) Andrew Haley
- [JDK-8374482](https://bugs.openjdk.org/browse/JDK-8374482) 8374482: SA does not handle signal handler frame in mixed jstack (+188/-10) Yasumasa Suenaga
- [JDK-8365292](https://bugs.openjdk.org/browse/JDK-8365292) 8365292: Remove javax.imageio.spi.ServiceRegistry.finalize() 8359391:  (+12/-184) Phil Race
- [JDK-8353950](https://bugs.openjdk.org/browse/JDK-8353950) 8353950: Clipboard interaction on Windows is unstable 8332271: Reading (+150/-46) Matthias Bläsing
- [JDK-8379153](https://bugs.openjdk.org/browse/JDK-8379153) 8379153: Refactor java/nio/channels/File{Channel,Lock} TestNG tests to (+91/-95) Brian Burkhalter
- [JDK-8367302](https://bugs.openjdk.org/browse/JDK-8367302) 8367302: New test jdk/jfr/event/profiling/TestCPUTimeSampleQueueAutoSi (+92/-91) Johannes Bechberger
- [JDK-8373867](https://bugs.openjdk.org/browse/JDK-8373867) 8373867: Improve robustness of Attach API for finding tmp directory (+154/-16) Yasumasa Suenaga
- [JDK-8372584](https://bugs.openjdk.org/browse/JDK-8372584) 8372584: [Linux]: Replace reading proc to get thread user CPU time wit (+96/-54) Jonas Norlinder
- [JDK-8321687](https://bugs.openjdk.org/browse/JDK-8321687) 8321687: Test vmTestbase/nsk/jvmti/scenarios/contention/TC03/tc03t002/ (+85/-57) Leonid Mesnik
- [JDK-8364764](https://bugs.openjdk.org/browse/JDK-8364764) 8364764: java/nio/channels/vthread/BlockingChannelOps.java subtests ti (+109/-31) Alan Bateman
- [JDK-8373127](https://bugs.openjdk.org/browse/JDK-8373127) 8373127: Update nsk/monitoring tests to support virtual thread factory (+87/-40) Leonid Mesnik
- [JDK-8379371](https://bugs.openjdk.org/browse/JDK-8379371) 8379371: Proposed cleanups for JDK-8373595 A new ObjectMonitorTable im (+58/-57) Daniel D. Daugherty
- [JDK-8379181](https://bugs.openjdk.org/browse/JDK-8379181) 8379181: Convert ObjectMonitorTable to use Atomic<T> (+60/-54) Axel Boldt-Christmas
- [JDK-8373367](https://bugs.openjdk.org/browse/JDK-8373367) 8373367: interp-only mechanism fails to work for carrier threads in a  (+61/-52) Serguei Spitsyn
- [JDK-8367137](https://bugs.openjdk.org/browse/JDK-8367137) 8367137: RISC-V: Detect Zicboz block size via hwprobe (+60/-50) Dingli Zhang
- [JDK-8367486](https://bugs.openjdk.org/browse/JDK-8367486) 8367486: Change prefix for platform-dependent AtomicAccess files (+52/-53) Stefan Karlsson
- [JDK-8371701](https://bugs.openjdk.org/browse/JDK-8371701) 8371701: Add ability to set NUMA-affinity for threads (+103/-0) Joel Sikström
- [JDK-8367796](https://bugs.openjdk.org/browse/JDK-8367796) 8367796: Rename AtomicAccess gtests (+52/-51) Kim Barrett
- [JDK-8376810](https://bugs.openjdk.org/browse/JDK-8376810) 8376810: Make Atomic<T> default constructor non-explicit (+95/-6) Stefan Karlsson
- [JDK-8361912](https://bugs.openjdk.org/browse/JDK-8361912) 8361912: ThreadsListHandle::cv_internal_thread_to_JavaThread  does not (+30/-66) David Holmes
- [JDK-8373106](https://bugs.openjdk.org/browse/JDK-8373106) 8373106: JFR suspend/resume deadlock on macOS in pthreads library (+44/-50) Markus Grönlund
- [JDK-8372625](https://bugs.openjdk.org/browse/JDK-8372625) 8372625: [Linux] Remove unnecessary logic for supports_fast_thread_cpu (+17/-75) Jonas Norlinder
- [JDK-8295851](https://bugs.openjdk.org/browse/JDK-8295851) 8295851: Do not use ttyLock in BytecodeTracer::trace (+55/-30) Coleen Phillimore
- [JDK-8376052](https://bugs.openjdk.org/browse/JDK-8376052) 8376052: Use AttachOperationFailedException rather than AttachNotSuppo (+47/-37) Yasumasa Suenaga
- [JDK-8359222](https://bugs.openjdk.org/browse/JDK-8359222) 8359222: [asan] jvmti/vthread/ToggleNotifyJvmtiTest/ToggleNotifyJvmtiT (+71/-13) Patricio Chilano Mateo
- [JDK-8376650](https://bugs.openjdk.org/browse/JDK-8376650) 8376650: os::release_memory_special may not be needed anymore (+12/-65) Casper Norrbin
- [JDK-8369997](https://bugs.openjdk.org/browse/JDK-8369997) 8369997: Tests that use custom scheduler should use jdk.test.lib.threa (+16/-60) Brian Burkhalter

*... 还有 127 个 Commits*

### JFR (86 Commits)

- [JDK-8369251](https://bugs.openjdk.org/browse/JDK-8369251) 8369251: Opensource few tests (+1102/-0) Prasanta Sadhukhan
- [JDK-8356698](https://bugs.openjdk.org/browse/JDK-8356698) 8356698: JFR: @Contextual (+703/-8) Erik Gahlin
- [JDK-8367949](https://bugs.openjdk.org/browse/JDK-8367949) 8367949: JFR: MethodTrace double-counts methods that catch their own e (+362/-30) Erik Gahlin
- [JDK-8365614](https://bugs.openjdk.org/browse/JDK-8365614) 8365614: JFR: Improve PrettyWriter::printValue (+88/-131) Erik Gahlin
- [JDK-8373490](https://bugs.openjdk.org/browse/JDK-8373490) 8373490: JFR Leak Profiler: path-to-gc-root very slow for large object (+202/-6) Thomas Stuefe
- [JDK-8362573](https://bugs.openjdk.org/browse/JDK-8362573) 8362573: Incorrect weight of the first ObjectAllocationSample JFR even (+147/-61) Markus Grönlund
- [JDK-8367107](https://bugs.openjdk.org/browse/JDK-8367107) 8367107: JFR: Refactor policy tests out of TestRemoteDump (+124/-74) Erik Gahlin
- [JDK-8364427](https://bugs.openjdk.org/browse/JDK-8364427) 8364427: JFR: Possible resource leak in Recording::getStream (+170/-16) Erik Gahlin
- [JDK-8373441](https://bugs.openjdk.org/browse/JDK-8373441) 8373441: Remove DCmdFactory::_enabled (+77/-98) Ioi Lam
- [JDK-8364190](https://bugs.openjdk.org/browse/JDK-8364190) 8364190: JFR: RemoteRecordingStream withers don't work (+151/-8) Erik Gahlin
- [JDK-8365823](https://bugs.openjdk.org/browse/JDK-8365823) 8365823: Revert storing abstract and interface Klasses to non-class me (+38/-97) Coleen Phillimore
- [JDK-8365611](https://bugs.openjdk.org/browse/JDK-8365611) 8365611: Use lookup table for JfrEventThrottler (+65/-45) Thomas Stuefe
- [JDK-8355960](https://bugs.openjdk.org/browse/JDK-8355960) 8355960: JvmtiAgentList::Iterator dtor double free with -fno-elide-con (+48/-60) Alex Menkov
- [JDK-8370715](https://bugs.openjdk.org/browse/JDK-8370715) 8370715: JFR: Races are possible when dumping recordings (+88/-1) Robert Toyonaga
- [JDK-8359687](https://bugs.openjdk.org/browse/JDK-8359687) 8359687: Use PassFailJFrame for java/awt/print/Dialog/DialogType.java (+51/-37) Srinivas Mandalika
- [JDK-8358750](https://bugs.openjdk.org/browse/JDK-8358750) 8358750: JFR: EventInstrumentation MASK_THROTTLE* constants should be  (+56/-30) Erik Gahlin
- [JDK-8379230](https://bugs.openjdk.org/browse/JDK-8379230) 8379230: JFR: Do not store leak context edge idx in markWord (+31/-52) Markus Grönlund
- [JDK-8360287](https://bugs.openjdk.org/browse/JDK-8360287) 8360287: JFR: PlatformTracer class should be loaded lazily (+64/-13) Erik Gahlin
- [JDK-8370884](https://bugs.openjdk.org/browse/JDK-8370884) 8370884: JFR: Overflow in aggregators (+58/-12) Erik Gahlin
- [JDK-8367772](https://bugs.openjdk.org/browse/JDK-8367772) 8367772: Refactor createUI in PassFailJFrame (+22/-47) Alexey Ivanov
- [JDK-8366809](https://bugs.openjdk.org/browse/JDK-8366809) 8366809: JFR: Use factory for aggregator functions (+38/-30) Erik Gahlin
- [JDK-8359242](https://bugs.openjdk.org/browse/JDK-8359242) 8359242: JFR: Missing help text for method trace and timing (+46/-15) Erik Gahlin
- [JDK-8372321](https://bugs.openjdk.org/browse/JDK-8372321) 8372321: TestBackToBackSensitive fails intermittently after JDK-836597 (+33/-26) Erik Gahlin
- [JDK-8369255](https://bugs.openjdk.org/browse/JDK-8369255) 8369255: Assess and remedy any unsafe usage of the Semaphores used by  (+38/-18) Markus Grönlund
- [JDK-8358590](https://bugs.openjdk.org/browse/JDK-8358590) 8358590: JFR: Include min and max in MethodTiming event (+49/-7) Erik Gahlin
- [JDK-8358205](https://bugs.openjdk.org/browse/JDK-8358205) 8358205: Remove unused JFR array allocation code (+5/-50) Coleen Phillimore
- [JDK-8364667](https://bugs.openjdk.org/browse/JDK-8364667) 8364667: JFR: Throttle doesn't work with dynamic events (+48/-6) Erik Gahlin
- [JDK-8378171](https://bugs.openjdk.org/browse/JDK-8378171) 8378171: JFR: Copy of a closed recording should not be available (+39/-14) Erik Gahlin
- [JDK-8374490](https://bugs.openjdk.org/browse/JDK-8374490) 8374490: Test jdk/jfr/event/runtime/TestSafepointEvents.java failed: E (+18/-31) Markus Grönlund
- [JDK-8364756](https://bugs.openjdk.org/browse/JDK-8364756) 8364756: JFR: Improve slow tests (+20/-20) Erik Gahlin
- [JDK-8367948](https://bugs.openjdk.org/browse/JDK-8367948) 8367948: JFR: MethodTrace threshold setting has no effect (+34/-5) Erik Gahlin
- [JDK-8368563](https://bugs.openjdk.org/browse/JDK-8368563) 8368563: JFR: Improve jfr query help text (+17/-16) Erik Gahlin
- [JDK-8365815](https://bugs.openjdk.org/browse/JDK-8365815) 8365815: JFR: Update metadata.xml with 'jfr query' examples (+29/-4) Erik Gahlin
- [JDK-8361338](https://bugs.openjdk.org/browse/JDK-8361338) 8361338: JFR: Min and max time in MethodTime event is confusing (+26/-7) Erik Gahlin
- [JDK-8373062](https://bugs.openjdk.org/browse/JDK-8373062) 8373062: JFR build failure with CDS disabled (+18/-13) Markus Grönlund
- [JDK-8369441](https://bugs.openjdk.org/browse/JDK-8369441) 8369441: Two container tests fail after JDK-8292984 (+10/-20) Severin Gehwolf
- [JDK-8346886](https://bugs.openjdk.org/browse/JDK-8346886) 8346886: Add since checker test to jdk.management.jfr (+30/-0) Nizar Benalla
- [JDK-8358602](https://bugs.openjdk.org/browse/JDK-8358602) 8358602: JFR: Annotations in jdk.jfr package should not use "not null" (+15/-15) Erik Gahlin
- [JDK-8364461](https://bugs.openjdk.org/browse/JDK-8364461) 8364461: JFR: Default constructor may not be first in setting control (+21/-8) Erik Gahlin
- [JDK-8373122](https://bugs.openjdk.org/browse/JDK-8373122) 8373122: JFR build failure with CDS disabled due to -Werror=unused-fun (+14/-14) Hao Sun
- [JDK-8368809](https://bugs.openjdk.org/browse/JDK-8368809) 8368809: JFR: Remove events from testSettingConfiguration in TestActiv (+5/-23) Erik Gahlin
- [JDK-8367348](https://bugs.openjdk.org/browse/JDK-8367348) 8367348: Enhance PassFailJFrame to support links in HTML (+23/-2) Weijun Wang
- [JDK-8365044](https://bugs.openjdk.org/browse/JDK-8365044) 8365044: Missing copyright header in Contextual.java (+25/-0) Dmitry Cherepanov
- [JDK-8360039](https://bugs.openjdk.org/browse/JDK-8360039) 8360039: JFR: Improve parser logging of constants (+20/-5) Erik Gahlin
- [JDK-8360518](https://bugs.openjdk.org/browse/JDK-8360518) 8360518: Docker tests do not work when asan is configured (+23/-0) Matthias Baesken
- [JDK-8361175](https://bugs.openjdk.org/browse/JDK-8361175) 8361175: JFR: Document differences between method sample events (+12/-10) Erik Gahlin
- [JDK-8359135](https://bugs.openjdk.org/browse/JDK-8359135) 8359135: New test TestCPUTimeSampleThrottling fails intermittently (+14/-8) Johannes Bechberger
- [JDK-8357993](https://bugs.openjdk.org/browse/JDK-8357993) 8357993: Use "stdin.encoding" for reading System.in with InputStreamRe (+13/-9) Volkan Yazici
- [JDK-8377665](https://bugs.openjdk.org/browse/JDK-8377665) 8377665: JFR: Symbol table not setup for early class unloading (+14/-7) Markus Grönlund
- [JDK-8372441](https://bugs.openjdk.org/browse/JDK-8372441) 8372441: JFR: Improve logging of TestBackToBackSensitive (+12/-9) Erik Gahlin

*... 还有 36 个 Commits*

### BUILD (153 Commits)

- [JDK-8379626](https://bugs.openjdk.org/browse/JDK-8379626) 8379626: Refactor jaxp/functional/javax/xml tests to use JUnit (+1681/-2053) David Beaumont
- [JDK-8367157](https://bugs.openjdk.org/browse/JDK-8367157) 8367157: Remove jrunscript tool (+4/-2364) Jaikiran Pai
- [JDK-8361076](https://bugs.openjdk.org/browse/JDK-8361076) 8361076: Add benchmark for ImageReader in preparation for Valhalla cha (+1080/-0) David Beaumont
- [JDK-8368714](https://bugs.openjdk.org/browse/JDK-8368714) 8368714: [BACKOUT] JDK-8368468 Split out everything but configure resu (+466/-525) Daniel D. Daugherty
- [JDK-8368468](https://bugs.openjdk.org/browse/JDK-8368468) 8368468: Split out everything but configure results from spec.gmk (+525/-466) Magnus Ihse Bursie
- [JDK-8370126](https://bugs.openjdk.org/browse/JDK-8370126) 8370126: Improve jpackage signing testing (+679/-269) Alexey Semenyuk
- [JDK-8356137](https://bugs.openjdk.org/browse/JDK-8356137) 8356137: GifImageDecode can produce opaque image when disposal method  (+618/-1) jeremy
- [JDK-8367259](https://bugs.openjdk.org/browse/JDK-8367259) 8367259: Clean up make/scripts and bin directory (+43/-470) Magnus Ihse Bursie
- [JDK-8364564](https://bugs.openjdk.org/browse/JDK-8364564) 8364564: Shortcut configuration is not recorded in .jpackage.xml file (+329/-121) Alexey Semenyuk
- [JDK-8370136](https://bugs.openjdk.org/browse/JDK-8370136) 8370136: Support async execution of jpackage tests (+299/-147) Alexey Semenyuk
- [JDK-8372359](https://bugs.openjdk.org/browse/JDK-8372359) 8372359: Clean jpackage error messages (+163/-192) Alexey Semenyuk
- [JDK-8373710](https://bugs.openjdk.org/browse/JDK-8373710) 8373710: Improve jpackage error reporting (+256/-20) Alexey Semenyuk
- [JDK-8372292](https://bugs.openjdk.org/browse/JDK-8372292) 8372292: Remove redundant "throws ConfigException" (+88/-162) Alexey Semenyuk
- [JDK-8369393](https://bugs.openjdk.org/browse/JDK-8369393) 8369393: NMT: poison the malloc header and footer under ASAN build (+151/-69) Afshin Zafari
- [JDK-8363979](https://bugs.openjdk.org/browse/JDK-8363979) 8363979: Add JDK bundle/image validation for --runtime-image option (+167/-41) Alexey Semenyuk
- [JDK-8341735](https://bugs.openjdk.org/browse/JDK-8341735) 8341735: Rewrite the build/AbsPathsInImage.java test to not load the e (+145/-58) Daniel Hu
- [JDK-8369328](https://bugs.openjdk.org/browse/JDK-8369328) 8369328: Use uppercase variable names in the devkit makefiles (+98/-98) Mikael Vidstedt
- [JDK-8357034](https://bugs.openjdk.org/browse/JDK-8357034) 8357034: GifImageDecoder can produce wrong transparent pixels (+147/-39) Jeremy Wood
- [JDK-8365053](https://bugs.openjdk.org/browse/JDK-8365053) 8365053: Refresh hotspot precompiled.hpp with headers based on current (+122/-46) Francesco Andreuzzi
- [JDK-8374471](https://bugs.openjdk.org/browse/JDK-8374471) 8374471: Check bin and lib folder of JDK image for unwanted files (+152/-0) Matthias Baesken
- [JDK-8370120](https://bugs.openjdk.org/browse/JDK-8370120) 8370120: Make jpackage tests output more stable (+98/-49) Alexey Semenyuk
- [JDK-8351842](https://bugs.openjdk.org/browse/JDK-8351842) 8351842: Windows specific issues in combination of JEP 493 and --with- (+56/-67) Christoph Langer
- [JDK-8368102](https://bugs.openjdk.org/browse/JDK-8368102) 8368102: Don't store macros in spec.gmk (+69/-48) Magnus Ihse Bursie
- [JDK-8332872](https://bugs.openjdk.org/browse/JDK-8332872) 8332872: SetupExecute should cd to temp directory (+101/-15) Magnus Ihse Bursie
- [JDK-8373909](https://bugs.openjdk.org/browse/JDK-8373909) 8373909: JSpec and ToolGuide taglets use incorrect relative path (+46/-66) Dan Smith
- [JDK-8366777](https://bugs.openjdk.org/browse/JDK-8366777) 8366777: Build fails unknown pseudo-op with old AS on linux-aarch64 (+57/-42) SendaoYan
- [JDK-8343546](https://bugs.openjdk.org/browse/JDK-8343546) 8343546: GHA: Cache required dependencies in master-branch workflow (+92/-3) Aleksey Shipilev
- [JDK-8356218](https://bugs.openjdk.org/browse/JDK-8356218) 8356218: [macos] Document --app-content (+80/-9) Alexander Matveev
- [JDK-8373246](https://bugs.openjdk.org/browse/JDK-8373246) 8373246: JDK-8351842 broke native debugging on Linux (+29/-59) Christoph Langer
- [JDK-8376892](https://bugs.openjdk.org/browse/JDK-8376892) 8376892: Allow conversion warnings in subsets of the code base (+74/-4) Leo Korinth
- [JDK-8370154](https://bugs.openjdk.org/browse/JDK-8370154) 8370154: Update @jls and @jvms taglets to point to local specs dir (+49/-23) Dan Smith
- [JDK-8367034](https://bugs.openjdk.org/browse/JDK-8367034) 8367034: [REDO] Protect ExecuteWithLog from running with redirection w (+39/-30) Magnus Ihse Bursie
- [JDK-8368326](https://bugs.openjdk.org/browse/JDK-8368326) 8368326: Don't export unresolved make variables from configure (+25/-38) Magnus Ihse Bursie
- [JDK-8367035](https://bugs.openjdk.org/browse/JDK-8367035) 8367035: [BACKOUT] Protect ExecuteWithLog from running with redirectio (+27/-36) David Holmes
- [JDK-8233115](https://bugs.openjdk.org/browse/JDK-8233115) 8233115: Protect ExecuteWithLog from running with redirection without  (+36/-27) Magnus Ihse Bursie
- [JDK-8369454](https://bugs.openjdk.org/browse/JDK-8369454) 8369454: Verify checksums of downloaded source bundles when creating d (+46/-15) Mikael Vidstedt
- [JDK-8365501](https://bugs.openjdk.org/browse/JDK-8365501) 8365501: Remove special AdapterHandlerEntry for abstract methods (+17/-44) Ashutosh Mehra
- [JDK-8375458](https://bugs.openjdk.org/browse/JDK-8375458) 8375458: Check legal folder of JDK image for unwanted files (+58/-1) Matthias Baesken
- [JDK-8377425](https://bugs.openjdk.org/browse/JDK-8377425) 8377425: Test runtime/os/TestWXHealing.java fails on macosx-aarch64 pr (+50/-8) Jaikiran Pai
- [JDK-8246325](https://bugs.openjdk.org/browse/JDK-8246325) 8246325: Add DRYRUN facility to SetupExecute (+46/-12) Magnus Ihse Bursie
- [JDK-8364560](https://bugs.openjdk.org/browse/JDK-8364560) 8364560: The default value of --linux-menu-group option is invalid 835 (+41/-12) Alexey Semenyuk
- [JDK-8361142](https://bugs.openjdk.org/browse/JDK-8361142) 8361142: Improve custom hooks for makefiles (+38/-14) Magnus Ihse Bursie
- [JDK-8370438](https://bugs.openjdk.org/browse/JDK-8370438) 8370438: Offer link time optimization support on library level (+37/-14) Matthias Baesken
- [JDK-8371440](https://bugs.openjdk.org/browse/JDK-8371440) 8371440: jpackage should exit with an error if it finds multiple match (+29/-20) Alexey Semenyuk
- [JDK-8377769](https://bugs.openjdk.org/browse/JDK-8377769) 8377769: Only use large pages sizes that have any pages configured (+34/-10) Leo Korinth
- [JDK-8362243](https://bugs.openjdk.org/browse/JDK-8362243) 8362243: Devkit creation for Fedora base OS is broken (+26/-15) Volkan Yazici
- [JDK-8377013](https://bugs.openjdk.org/browse/JDK-8377013) 8377013: TimeZone.getDefault() returns obsolete id on Windows (Asia/Ca (+34/-5) Naoto Sato
- [JDK-8371914](https://bugs.openjdk.org/browse/JDK-8371914) 8371914: PNG defines in CFLAGS can cause compilation errors with exter (+19/-19) Kurt Miller
- [JDK-8374990](https://bugs.openjdk.org/browse/JDK-8374990) 8374990: Check include and jmods folder of JDK image for unwanted file (+35/-2) Matthias Baesken
- [JDK-8374767](https://bugs.openjdk.org/browse/JDK-8374767) 8374767: Amend JDK-8374521 with new option name (+18/-18) Aleksey Shipilev

*... 还有 103 个 Commits*
