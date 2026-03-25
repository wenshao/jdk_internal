# Release Notes 追踪

> 469 个标记 release-note=yes 的 PR

---

## 按版本

### JDK 26 (35 条)

| Bug ID | 标题 | Author | 组织 | 优先级 | 组件 |
|--------|------|--------|------|--------|------|
| [8366434](../../by-pr/8366/8366434.md) | THP not working properly with G1 after JDK-8345655 | kstefanj | Oracle | P2 | hotspot |
| [8367031](../../by-pr/8367/8367031.md) | [backout] Change java.time month/day field types to 'by | RogerRiggs | Oracle | P2 | core-libs |
| [8365057](../../by-pr/8365/8365057.md) | Add support for java.util.concurrent lock information t | alexmenkov | Oracle | P2 | hotspot |
| [8314323](../../by-pr/8314/8314323.md) | Implement JEP 527: TLS 1.3 Hybrid Key Exchange | haimaychao | Oracle | P2 | security-libs |
| [8354469](../../by-pr/8354/8354469.md) | Keytool exposes the password in plain text when command | wangweij | Oracle | P3 | security-libs |
| [8208693](../../by-pr/8208/8208693.md) | HttpClient: Extend the request timeout's scope to cover | vy | Oracle | P3 | core-libs |
| [8353749](../../by-pr/8353/8353749.md) | Improve security warning when using JKS or JCEKS keysto | haimaychao | Oracle | P3 | security-libs |
| [8369238](../../by-pr/8369/8369238.md) | Allow virtual thread preemption on some common class in | pchilano | Oracle | P3 | hotspot |
| [8369736](../../by-pr/8369/8369736.md) | - Add management interface for AOT cache creation | macarte |  | P3 | core-svc |
| [8347831](../../by-pr/8347/8347831.md) | Re-examine version check when cross linking | slowhog | Oracle | P3 | tools |
| [8369736](../../by-pr/8369/8369736.md) | Add management interface for AOT cache creation | iklam | Oracle | P3 | core-svc |
| [8366911](../../by-pr/8366/8366911.md) | (fs) Remove support for normalizing file names to Unico | bplb | Oracle | P4 | core-libs |
| [8367157](../../by-pr/8367/8367157.md) | Remove jrunscript tool | jaikiran | Oracle | P4 | tools |
| [8367112](../../by-pr/8367/8367112.md) | HttpClient does not support Named Groups set on SSLPara | djelinski | Oracle | P4 | core-libs |
| [8368226](../../by-pr/8368/8368226.md) | Remove Thread.stop | AlanBateman | Oracle | P4 | core-libs |
| [8048180](../../by-pr/8048/8048180.md) | G1: Eager reclaim of humongous objects with references | tschatzl | Oracle | P4 | hotspot |
| [8366829](../../by-pr/8366/8366829.md) | Add java.time.Duration constants MIN and MAX | pavelrappo | Oracle | P4 | core-libs |
| [8368527](../../by-pr/8368/8368527.md) | JMX: Add an MXBeans method to query GC CPU time | JonasNorlinder |  | P4 | core-svc |
| [7105350](../../by-pr/7105/7105350.md) | HttpExchange's attributes are the same as HttpContext's | SentryMan |  | P4 | core-libs |
| [8362637](../../by-pr/8362/8362637.md) | Convert java.nio.ByteOrder to an enum | RogerRiggs | Oracle | P4 | core-libs |

> 共 35 条，仅显示前 20

### JDK 25 (63 条)

| Bug ID | 标题 | Author | 组织 | 优先级 | 组件 |
|--------|------|--------|------|--------|------|
| [8340321](../../by-pr/8340/8340321.md) | Disable SHA-1 in TLS/DTLS 1.2 handshake signatures | artur-oracle | Oracle | P2 | security-libs |
| [8343232](../../by-pr/8343/8343232.md) | PKCS#12 KeyStore support for RFC 9879: Use of Password- | mcpowers | Oracle | P2 | security-libs |
| [8359170](../../by-pr/8359/8359170.md) | Add 2 TLS and 2 CS Sectigo roots | rhalade | Oracle | P2 | security-libs |
| [8359170](../../by-pr/8359/8359170.md) | Add 2 TLS and 2 CS Sectigo roots | rhalade | Oracle | P2 | security-libs |
| [8303770](../../by-pr/8303/8303770.md) | Remove Baltimore root certificate expiring in May 2025 | rhalade | Oracle | P3 | security-libs |
| [8348732](../../by-pr/8348/8348732.md) | SunJCE and SunPKCS11 have different PBE key encodings | valeriepeng | Oracle | P3 | security-libs |
| [8346948](../../by-pr/8346/8346948.md) | Update CLDR to Version 47.0 | naotoj | Oracle | P3 | core-libs |
| [8348282](../../by-pr/8348/8348282.md) | Add option for syntax highlighting in javadoc snippets | hns | Oracle | P3 | tools |
| [8348967](../../by-pr/8348/8348967.md) | Deprecate security permission classes for removal | seanjmullan | Oracle | P3 | security-libs |
| [8350457](../../by-pr/8350/8350457.md) | Implement JEP 519: Compact Object Headers | rkennke | Datadog | P3 | hotspot |
| [8322810](../../by-pr/8322/8322810.md) | Lambda expression types can't be classes | vicente-romero-oracle | Oracle | P3 | tools |
| [8354305](../../by-pr/8354/8354305.md) | SHAKE128 and SHAKE256 MessageDigest algorithms | wangweij | Oracle | P3 | security-libs |
| [8356698](../../by-pr/8356/8356698.md) | JFR: @Contextual | egahlin | Oracle | P3 | hotspot |
| [8356870](../../by-pr/8356/8356870.md) | HotSpotDiagnosticMXBean.dumpThreads and jcmd Thread.dum | AlanBateman | Oracle | P3 | core-svc |
| [8353925](../../by-pr/8353/8353925.md) | Remove Sun Microsystems JCE Code Signing Root CA | bradfordwetmore | Oracle | P3 | security-libs |
| [8361640](../../by-pr/8361/8361640.md) | JFR: RandomAccessFile::readLine emits events for each c | egahlin | Oracle | P3 | hotspot |
| [8356557](../../by-pr/8356/8356557.md) | Update CodeSource::implies API documentation and deprec | seanjmullan | Oracle | P3 | security-libs |
| [8361640](../../by-pr/8361/8361640.md) | JFR: RandomAccessFile::readLine emits events for each c | egahlin | Oracle | P3 | hotspot |
| [8244336](../../by-pr/8244/8244336.md) | Restrict algorithms at JCE layer | valeriepeng | Oracle | P3 | security-libs |
| [8361964](../../by-pr/8361/8361964.md) | Remove outdated algorithms from requirements and add PB | seanjmullan | Oracle | P3 | security-libs |

> 共 63 条，仅显示前 20

### JDK 24 (28 条)

| Bug ID | 标题 | Author | 组织 | 优先级 | 组件 |
|--------|------|--------|------|--------|------|
| [8341057](../../by-pr/8341/8341057.md) | Add 2 SSL.com TLS roots | rhalade | Oracle | P2 | security-libs |
| [8338890](../../by-pr/8338/8338890.md) | Add monitoring/management interface for the virtual thr | AlanBateman | Oracle | P3 | core-svc |
| [8326949](../../by-pr/8326/8326949.md) | Authorization header is removed when a proxy Authentica | Michael-Mc-Mahon | Oracle | P3 | core-libs |
| [8341964](../../by-pr/8341/8341964.md) | Add mechanism to disable different parts of TLS cipher  | artur-oracle | Oracle | P3 | security-libs |
| [8341553](../../by-pr/8341/8341553.md) | Remove UseCompactObjectHeaders extra CDS archives | calvinccheung | Oracle | P3 | hotspot |
| [8343791](../../by-pr/8343/8343791.md) | Socket.connect API should document whether the socket w | vy | Oracle | P3 | core-libs |
| [8245545](../../by-pr/8245/8245545.md) | Disable TLS_RSA cipher suites | artur-oracle | Oracle | P3 | security-libs |
| [8344041](../../by-pr/8344/8344041.md) | Re-enable external specs page | hns | Oracle | P3 | tools |
| [8341551](../../by-pr/8341/8341551.md) | Revisit jdk.internal.loader.URLClassPath.JarLoader afte | jaikiran | Oracle | P3 | core-libs |
| [8338894](../../by-pr/8338/8338894.md) | Deprecate jhsdb debugd for removal | kevinjwalls | Oracle | P4 | hotspot |
| [8334165](../../by-pr/8334/8334165.md) | Remove serialVersionUID compatibility logic from JMX | kevinjwalls | Oracle | P4 | core-svc |
| [8339918](../../by-pr/8339/8339918.md) | Remove checks for outdated -t -tm -Xfuture -checksource | jaikiran | Oracle | P4 | tools |
| [8286851](../../by-pr/8286/8286851.md) | Deprecate for removal several of the undocumented java  | jaikiran | Oracle | P4 | tools |
| [8341566](../../by-pr/8341/8341566.md) | Add Reader.of(CharSequence) | mkarg |  | P4 | core-libs |
| [8341134](../../by-pr/8341/8341134.md) | Deprecate for removal the jrunscript tool | jaikiran | Oracle | P4 | tools |
| [8340477](../../by-pr/8340/8340477.md) | Remove JDK1.1 compatible behavior for "EST"; "MST"; and | naotoj | Oracle | P4 | core-libs |
| [8342075](../../by-pr/8342/8342075.md) | HttpClient: improve HTTP/2 flow control checks | dfuch | Oracle | P4 | core-libs |
| [8343110](../../by-pr/8343/8343110.md) | Add getChars(int; int; char[]; int) to CharSequence and | mkarg |  | P4 | core-libs |
| [8330606](../../by-pr/8330/8330606.md) | Redefinition doesn't but should verify the new klass | coleenp | Oracle | P4 | hotspot |
| [8338536](../../by-pr/8338/8338536.md) | Permanently disable remote code downloading in JNDI | AlekseiEfimov |  | P4 | core-libs |

> 共 28 条，仅显示前 20

### JDK 23 (59 条)

| Bug ID | 标题 | Author | 组织 | 优先级 | 组件 |
|--------|------|--------|------|--------|------|
| [8322750](../../by-pr/8322/8322750.md) | Test "api/java_awt/interactive/SystemTrayTests.html" fa | azvegint | Oracle | P1 | client-libs |
| [8338139](../../by-pr/8338/8338139.md) | {ClassLoading;Memory}MXBean::isVerbose methods are inco | stefank | Oracle | P1 | core-svc |
| [8338139](../../by-pr/8338/8338139.md) | {ClassLoading;Memory}MXBean::isVerbose methods are inco | stefank | Oracle | P1 | core-svc |
| [8328744](../../by-pr/8328/8328744.md) | Parallel: Parallel GC throws OOM before heap is fully e | zhengyu123 | Datadog | P2 | hotspot |
| [8295111](../../by-pr/8295/8295111.md) | dpkg appears to have problems resolving symbolically li | alexeysemenyukoracle | Oracle | P2 | tools |
| [8321408](../../by-pr/8321/8321408.md) | Add Certainly roots R1 and E1 | rhalade | Oracle | P3 | security-libs |
| [8256314](../../by-pr/8256/8256314.md) | JVM TI GetCurrentContendedMonitor is implemented incorr | sspitsyn | Oracle | P3 | hotspot |
| [8326666](../../by-pr/8326/8326666.md) | Remove the Java Management Extension (JMX) Subject Dele | kevinjwalls | Oracle | P3 | core-svc |
| [8293345](../../by-pr/8293/8293345.md) | SunPKCS11 provider checks on PKCS11 Mechanism are probl | valeriepeng | Oracle | P3 | security-libs |
| [8325448](../../by-pr/8325/8325448.md) | Hybrid Public Key Encryption | wangweij | Oracle | P3 | security-libs |
| [6968351](../../by-pr/6968/6968351.md) | httpserver clashes with delayed TCP ACKs for low Conten | robaho |  | P3 | core-libs |
| [8044609](../../by-pr/8044/8044609.md) | javax.net.debug options not working and documented as e | coffeys | Oracle | P3 | security-libs |
| [8319990](../../by-pr/8319/8319990.md) | Update CLDR to Version 45.0 | naotoj | Oracle | P3 | core-libs |
| [8309881](../../by-pr/8309/8309881.md) | Qualified name of a type element depends on its origin  | asotona | Oracle | P3 | tools |
| [8328083](../../by-pr/8328/8328083.md) | degrade virtual thread support for GetObjectMonitorUsag | sspitsyn | Oracle | P3 | hotspot |
| [8316138](../../by-pr/8316/8316138.md) | Add GlobalSign 2 TLS root certificates | rhalade | Oracle | P3 | security-libs |
| [8321314](../../by-pr/8321/8321314.md) | Reinstate disabling the compiler's default active annot | jddarcy | Oracle | P3 | tools |
| [8309841](../../by-pr/8309/8309841.md) | Jarsigner should print a warning if an entry is removed | wangweij | Oracle | P3 | security-libs |
| [8335638](../../by-pr/8335/8335638.md) | Calling VarHandle.{access-mode} methods reflectively th | SirYwell |  | P3 | core-libs |
| [8336492](../../by-pr/8336/8336492.md) | Regression in lambda serialization | mcimadamore | Oracle | P3 | tools |

> 共 59 条，仅显示前 20

### JDK 22 (9 条)

| Bug ID | 标题 | Author | 组织 | 优先级 | 组件 |
|--------|------|--------|------|--------|------|
| [8315810](../../by-pr/8315/8315810.md) | Reimplement sun.reflect.ReflectionFactory::newConstruct | mlchung | Oracle | P3 | core-libs |
| [8296246](../../by-pr/8296/8296246.md) | Update Unicode Data Files to Version 15.1.0 | naotoj | Oracle | P3 | core-libs |
| [8316304](../../by-pr/8316/8316304.md) | (fs) Add support for BasicFileAttributes.creationTime() | jerboaa | IBM | P3 | core-libs |
| [8287843](../../by-pr/8287/8287843.md) | File::getCanonicalFile doesn't work for \\?\C:\ style p | bplb | Oracle | P4 | core-libs |
| [8315938](../../by-pr/8315/8315938.md) | Deprecate for removal Unsafe methods that have standard | AlanBateman | Oracle | P4 | core-libs |
| [8316160](../../by-pr/8316/8316160.md) | Remove sun.misc.Unsafe.{shouldBeInitialized;ensureClass | AlanBateman | Oracle | P4 | core-libs |
| [8316735](../../by-pr/8316/8316735.md) | Print LockStack in hs_err files | TheRealMDoerr | SAP | P4 | hotspot |
| [8309356](../../by-pr/8309/8309356.md) | Read files in includedir in alphanumeric order | wangweij | Oracle | P4 | security-libs |
| [8316971](../../by-pr/8316/8316971.md) | Add Lint warning for restricted method calls | mcimadamore | Oracle | P4 | tools |

### JDK 21 (79 条)

| Bug ID | 标题 | Author | 组织 | 优先级 | 组件 |
|--------|------|--------|------|--------|------|
| [8311981](../../by-pr/8311/8311981.md) | Test gc/stringdedup/TestStringDeduplicationAgeThreshold | dholmes-ora | Oracle | P2 | hotspot |
| [8313765](../../by-pr/8313/8313765.md) | Invalid CEN header (invalid zip64 extra data field size | LanceAndersen | Oracle | P2 | core-libs |
| [8314960](../../by-pr/8314/8314960.md) | Add Certigna Root CA - 2 | rhalade | Oracle | P2 | security-libs |
| [8208077](../../by-pr/8208/8208077.md) | File.listRoots performance degradation | AlanBateman | Oracle | P3 | core-libs |
| [8301260](../../by-pr/8301/8301260.md) | Add system property to toggle XML Signature secure vali | seanjmullan | Oracle | P3 | security-libs |
| [8245654](../../by-pr/8245/8245654.md) | Add Certigna Root CA | rhalade | Oracle | P3 | security-libs |
| [8301700](../../by-pr/8301/8301700.md) | Increase the default TLS Diffie-Hellman group size from | seanjmullan | Oracle | P3 | security-libs |
| [8301627](../../by-pr/8301/8301627.md) | System.exit and Runtime.exit debug logging | RogerRiggs | Oracle | P3 | core-libs |
| [8303530](../../by-pr/8303/8303530.md) | Redefine JAXP Configuration File | JoeWang-Java | Oracle | P3 | xml |
| [8305091](../../by-pr/8305/8305091.md) | Change ChaCha20 cipher init behavior to match AES-GCM | jnimeh | Oracle | P3 | security-libs |
| [8296248](../../by-pr/8296/8296248.md) | Update CLDR to Version 43.0 | naotoj | Oracle | P3 | core-libs |
| [8041676](../../by-pr/8041/8041676.md) | remove the java.compiler system property | jaikiran | Oracle | P3 | core-libs |
| [8306461](../../by-pr/8306/8306461.md) | ObjectInputStream::readObject() should handle negative  | simonis | Amazon | P3 | core-libs |
| [8298127](../../by-pr/8298/8298127.md) | HSS/LMS Signature Verification | ferakocz |  | P3 | security-libs |
| [8305975](../../by-pr/8305/8305975.md) | Add TWCA Global Root CA | rhalade | Oracle | P3 | security-libs |
| [8304760](../../by-pr/8304/8304760.md) | Add 2 Microsoft TLS roots | rhalade | Oracle | P3 | security-libs |
| [8307134](../../by-pr/8307/8307134.md) | Add GTS root CAs | jianglizhou | Oracle | P3 | security-libs |
| [8307779](../../by-pr/8307/8307779.md) | Relax the java.awt.Robot specification | azvegint | Oracle | P3 | client-libs |
| [8305972](../../by-pr/8305/8305972.md) | Update XML Security for Java to 3.0.2 | wangweij | Oracle | P3 | security-libs |
| [8307466](../../by-pr/8307/8307466.md) | java.time.Instant calculation bug in until and between  | RogerRiggs | Oracle | P3 | core-libs |

> 共 79 条，仅显示前 20

### JDK 20 (26 条)

| Bug ID | 标题 | Author | 组织 | 优先级 | 组件 |
|--------|------|--------|------|--------|------|
| [8290367](../../by-pr/8290/8290367.md) | Update default value and extend the scope of com.sun.jn | AlekseiEfimov | Oracle | P3 | core-libs |
| [8283093](../../by-pr/8283/8283093.md) | JMX connections should default to using an ObjectInputF | kevinjwalls | Oracle | P3 | core-svc |
| [8293590](../../by-pr/8293/8293590.md) | Some syntax checks performed by URL.openConnection() co | dfuch | Oracle | P3 | core-libs |
| [8290368](../../by-pr/8290/8290368.md) | Introduce LDAP and RMI protocol-specific object factory | AlekseiEfimov | Oracle | P3 | core-libs |
| [8288387](../../by-pr/8288/8288387.md) | GetLocalXXX/SetLocalXXX spec should require suspending  | sspitsyn | Oracle | P3 | hotspot |
| [8284840](../../by-pr/8284/8284840.md) | Update CLDR to Version 42.0 | naotoj | Oracle | P3 | core-libs |
| [8295673](../../by-pr/8295/8295673.md) | Deprecate and disable legacy parallel class loading wor | coleenp | Oracle | P3 | hotspot |
| [8284842](../../by-pr/8284/8284842.md) | Update Unicode Data Files to Version 15.0.0 | naotoj | Oracle | P3 | core-libs |
| [8289689](../../by-pr/8289/8289689.md) | (fs) Re-examine the need for normalization to Unicode N | bplb | Oracle | P3 | core-libs |
| [8256660](../../by-pr/8256/8256660.md) | Disable DTLS 1.0 | seanjmullan | Oracle | P3 | security-libs |
| [8279164](../../by-pr/8279/8279164.md) | Disable TLS_ECDH_* cipher suites | seanjmullan | Oracle | P3 | security-libs |
| [8297118](../../by-pr/8297/8297118.md) | Change IncompatibleClassChangeError to MatchException f | lahodaj | Oracle | P3 | tools |
| [8297276](../../by-pr/8297/8297276.md) | Remove thread text from Subject.current | wangweij | Oracle | P3 | security-libs |
| [8288717](../../by-pr/8288/8288717.md) | Add a means to close idle connections in HTTP/2 connect | c-cleary | Oracle | P4 | core-libs |
| [8293499](../../by-pr/8293/8293499.md) | Provide jmod --compress option | shipilev | Amazon | P4 | tools |
| [8289610](../../by-pr/8289/8289610.md) | Degrade Thread.stop | AlanBateman | Oracle | P4 | core-libs |
| [8249627](../../by-pr/8249/8249627.md) | Degrade Thread.suspend and Thread.resume | AlanBateman | Oracle | P4 | core-libs |
| [8292177](../../by-pr/8292/8292177.md) | InitialSecurityProperty JFR event | coffeys | Oracle | P4 | security-libs |
| [8288047](../../by-pr/8288/8288047.md) | Accelerate Poly1305 on x86_64 using AVX512 instructions | vpaprotsk | Intel | P4 | hotspot |
| [6924219](../../by-pr/6924/6924219.md) | (fc spec) FileChannel.write(ByteBuffer; position) behav | bplb | Oracle | P4 | core-libs |

> 共 26 条，仅显示前 20

### JDK 19 (50 条)

| Bug ID | 标题 | Author | 组织 | 优先级 | 组件 |
|--------|------|--------|------|--------|------|
| [8292327](../../by-pr/8292/8292327.md) | java.io.EOFException in InflaterInputStream after JDK-8 | simonis | SAP | P2 | core-libs |
| [8268081](../../by-pr/8268/8268081.md) | Upgrade Unicode Data Files to 14.0.0 | naotoj | Oracle | P3 | core-libs |
| [8279842](../../by-pr/8279/8279842.md) | HTTPS Channel Binding support for Java GSS/Kerberos | Michael-Mc-Mahon | Oracle | P3 | core-libs |
| [8280494](../../by-pr/8280/8280494.md) | (D)TLS signature schemes | XueleiFan | Oracle | P3 | security-libs |
| [8281175](../../by-pr/8281/8281175.md) | Add a -providerPath option to jarsigner | wangweij | Oracle | P3 | security-libs |
| [8267319](../../by-pr/8267/8267319.md) | Use larger default key sizes and algorithms based on CN | valeriepeng | Oracle | P3 | security-libs |
| [8281181](../../by-pr/8281/8281181.md) | Do not use CPU Shares to compute active processor count | iklam | Oracle | P3 | hotspot |
| [8281561](../../by-pr/8281/8281561.md) | Disable http DIGEST mechanism with MD5 and SHA-1 by def | Michael-Mc-Mahon | Oracle | P3 | core-libs |
| [7192189](../../by-pr/7192/7192189.md) | Support endpoint identification algorithm in RFC 6125 | seanjmullan | Oracle | P3 | security-libs |
| [8247645](../../by-pr/8247/8247645.md) | ChaCha20 intrinsics | jnimeh | Oracle | P3 | security-libs |
| [8273553](../../by-pr/8273/8273553.md) | sun.security.ssl.SSLEngineImpl.closeInbound also has si | bradfordwetmore | Oracle | P3 | security-libs |
| [8254935](../../by-pr/8254/8254935.md) | Deprecate the PSSParameterSpec(int) constructor | valeriepeng | Oracle | P3 | security-libs |
| [8212136](../../by-pr/8212/8212136.md) | Remove finalizer implementation in SSLSocketImpl | XueleiFan | Oracle | P3 | security-libs |
| [8284378](../../by-pr/8284/8284378.md) | Make Metal the default Java 2D rendering pipeline for m | aghaisas |  | P3 | client-libs |
| [8265315](../../by-pr/8265/8265315.md) | Support for CLDR version 41 | naotoj | Oracle | P3 | core-libs |
| [8284161](../../by-pr/8284/8284161.md) | Implementation of Virtual Threads (Preview) | AlanBateman | Oracle | P3 | core-libs |
| [8178355](../../by-pr/8178/8178355.md) | IdentityHashMap uses identity-based comparison for valu | liach | Oracle | P3 | core-libs |
| [8285445](../../by-pr/8285/8285445.md) | cannot open file "NUL:" | bplb | Oracle | P3 | core-libs |
| [8286090](../../by-pr/8286/8286090.md) | Add RC2/RC4 to jdk.security.legacyAlgorithms | haimaychao | Oracle | P3 | security-libs |
| [8250950](../../by-pr/8250/8250950.md) | Allow per-user and system wide configuration of a jpack | alexeysemenyukoracle | Oracle | P3 | tools |

> 共 50 条，仅显示前 20

### JDK 18 (31 条)

| Bug ID | 标题 | Author | 组织 | 优先级 | 组件 |
|--------|------|--------|------|--------|------|
| [8277212](../../by-pr/8277/8277212.md) | GC accidentally cleans valid megamorphic vtable inline  | stefank | Oracle | P2 | hotspot |
| [8263773](../../by-pr/8263/8263773.md) | Reenable German localization for builds at Oracle | svijayasekar |  | P3 | globalization |
| [8264849](../../by-pr/8264/8264849.md) | Add KW and KWP support to PKCS11 provider | valeriepeng | Oracle | P3 | security-libs |
| [8273670](../../by-pr/8273/8273670.md) | Remove weak etypes from default krb5 etype list | wangweij | Oracle | P3 | security-libs |
| [8202056](../../by-pr/8202/8202056.md) | Expand serial warning to check for bad overloads of ser | jddarcy | Oracle | P3 | tools |
| [8274471](../../by-pr/8274/8274471.md) | Verification of OCSP Response signed with RSASSA-PSS fa | wangweij | Oracle | P3 | security-libs |
| [8274407](../../by-pr/8274/8274407.md) | (tz) Update Timezone Data to 2021c | naotoj | Oracle | P3 | core-libs |
| [8260428](../../by-pr/8260/8260428.md) | Drop support for pre JDK 1.4 DatagramSocketImpl impleme | pconcannon | Oracle | P3 | core-libs |
| [8275252](../../by-pr/8275/8275252.md) | Migrate cacerts from JKS to password-less PKCS12 | wangweij | Oracle | P3 | security-libs |
| [8231107](../../by-pr/8231/8231107.md) | Allow store password to be null when saving a PKCS12 Ke | wangweij | Oracle | P3 | security-libs |
| [8272163](../../by-pr/8272/8272163.md) | Add -version option to keytool and jarsigner | haimaychao | Oracle | P3 | security-libs |
| [8276665](../../by-pr/8276/8276665.md) | ObjectInputStream.GetField.get(name; object) should thr | RogerRiggs | Oracle | P3 | core-libs |
| [8276970](../../by-pr/8276/8276970.md) | Default charset for PrintWriter that wraps PrintStream | naotoj | Oracle | P3 | core-libs |
| [8278087](../../by-pr/8278/8278087.md) | Deserialization filter and filter factory property erro | RogerRiggs | Oracle | P3 | core-libs |
| [8255409](../../by-pr/8255/8255409.md) | Support the new C_GetInterfaceList; C_GetInterface; and | valeriepeng | Oracle | P3 | security-libs |
| [8272317](../../by-pr/8272/8272317.md) | jstatd has dependency on Security Manager which needs t | kevinjwalls | Oracle | P3 | core-svc |
| [8231640](../../by-pr/8231/8231640.md) | (prop) Canonical property storage | jaikiran | Oracle | P4 | core-libs |
| [8193682](../../by-pr/8193/8193682.md) | Infinite loop in ZipOutputStream.close() | raviniitw2012 |  | P4 | core-libs |
| [8273401](../../by-pr/8273/8273401.md) | Disable JarIndex support in URLClassPath | shiyuexw |  | P4 | core-libs |
| [8274227](../../by-pr/8274/8274227.md) | Remove "impl.prefix" jdk system property usage from Ine | AlekseiEfimov | Oracle | P4 | core-libs |

> 共 31 条，仅显示前 20

### JDK 17 (57 条)

| Bug ID | 标题 | Author | 组织 | 优先级 | 组件 |
|--------|------|--------|------|--------|------|
| [8196415](../../by-pr/8196/8196415.md) | Disable SHA-1 Signed JARs | seanjmullan | Oracle | P2 | security-libs |
| [8256895](../../by-pr/8256/8256895.md) | Add support for RFC 8954: Online Certificate Status Pro | haimaychao | Oracle | P3 | security-libs |
| [8259401](../../by-pr/8259/8259401.md) | Add checking to jarsigner to warn weak algorithms used  | haimaychao | Oracle | P3 | security-libs |
| [8259801](../../by-pr/8259/8259801.md) | Enable XML Signature secure validation mode by default | seanjmullan | Oracle | P3 | security-libs |
| [8256421](../../by-pr/8256/8256421.md) | Add 2 HARICA roots to cacerts truststore | rhalade | Oracle | P3 | security-libs |
| [8237352](../../by-pr/8237/8237352.md) | Update DatagramSocket to add support for joining multic | dfuch | Oracle | P3 | core-libs |
| [8257497](../../by-pr/8257/8257497.md) | Update keytool to create AKID from the SKID of the issu | haimaychao | Oracle | P3 | security-libs |
| [8235139](../../by-pr/8235/8235139.md) | Deprecate the socket impl factory mechanism | pconcannon | Oracle | P3 | core-libs |
| [8248268](../../by-pr/8248/8248268.md) | Support KWP in addition to KW | valeriepeng | Oracle | P3 | security-libs |
| [8259709](../../by-pr/8259/8259709.md) | Disable SHA-1 XML Signatures | seanjmullan | Oracle | P3 | security-libs |
| [8225081](../../by-pr/8225/8225081.md) | Remove Telia Company CA certificate expiring in April 2 | rhalade | Oracle | P3 | security-libs |
| [8261160](../../by-pr/8261/8261160.md) | Add a deserialization JFR event | ChrisHegarty |  | P3 | core-libs |
| [8139348](../../by-pr/8139/8139348.md) | Deprecate 3DES and RC4 in Kerberos | wangweij | Oracle | P3 | security-libs |
| [8173970](../../by-pr/8173/8173970.md) | jar tool should have a way to extract to a directory | jaikiran | Oracle | P3 | tools |
| [8182043](../../by-pr/8182/8182043.md) | Access to Windows Large Icons | azuev-java | Oracle | P3 | client-libs |
| [4511638](../../by-pr/4511/4511638.md) | Double.toString(double) sometimes produces incorrect re | rgiulietti | Oracle | P3 | core-libs |
| [8255410](../../by-pr/8255/8255410.md) | Add ChaCha20 and Poly1305 support to SunPKCS11 provider | valeriepeng | Oracle | P3 | security-libs |
| [8258794](../../by-pr/8258/8258794.md) | Support for CLDR version 39 | naotoj | Oracle | P3 | core-libs |
| [8260517](../../by-pr/8260/8260517.md) | implement Sealed Classes as a standard feature in Java | vicente-romero-oracle | Oracle | P3 | tools |
| [8240256](../../by-pr/8240/8240256.md) | Better resource cleaning for SunPKCS11 Provider | coffeys | Oracle | P3 | security-libs |

> 共 57 条，仅显示前 20

### JDK 16 (32 条)

| Bug ID | 标题 | Author | 组织 | 优先级 | 组件 |
|--------|------|--------|------|--------|------|
| [8202343](../../by-pr/8202/8202343.md) | Disable TLS 1.0 and 1.1 | seanjmullan | Oracle | P2 | security-libs |
| [8216497](../../by-pr/8216/8216497.md) | javadoc should auto-link to platform classes | hns | Oracle | P3 | tools |
| [8159746](../../by-pr/8159/8159746.md) | (proxy) Support for default methods | mlchung | Oracle | P3 | core-libs |
| [8242068](../../by-pr/8242/8242068.md) | Signed JAR support for RSASSA-PSS and EdDSA | wangweij | Oracle | P3 | security-libs |
| [8254177](../../by-pr/8254/8254177.md) | (tz) Upgrade time-zone data to tzdata2020b | kiranoracle |  | P3 | core-libs |
| [8212879](../../by-pr/8212/8212879.md) | Make JVMTI TagMap table concurrent | coleenp | Oracle | P3 | hotspot |
| [8251317](../../by-pr/8251/8251317.md) | Support for CLDR version 38 | naotoj | Oracle | P3 | core-libs |
| [8256643](../../by-pr/8256/8256643.md) | Terminally deprecate ThreadGroup stop; destroy; isDestr | AlanBateman | Oracle | P3 | core-libs |
| [8256299](../../by-pr/8256/8256299.md) | Implement JEP 396: Strongly Encapsulate JDK Internals b | mbreinhold |  | P3 | core-libs |
| [8243559](../../by-pr/8243/8243559.md) | Remove root certificates with 1024-bit keys | seanjmullan | Oracle | P3 | security-libs |
| [8254631](../../by-pr/8254/8254631.md) | Better support ALPN byte wire values in SunJSSE | bradfordwetmore | Oracle | P3 | security-libs |
| [8242332](../../by-pr/8242/8242332.md) | Add SHA3 support to SunPKCS11 provider | valeriepeng | Oracle | P3 | security-libs |
| [8257572](../../by-pr/8257/8257572.md) | Deprecate the archaic signal-chaining interfaces: sigse | dholmes-ora | Oracle | P3 | hotspot |
| [8165276](../../by-pr/8165/8165276.md) | Spec states to invoke the premain method in an agent cl | sspitsyn | Oracle | P3 | core-svc |
| [8246005](../../by-pr/8246/8246005.md) | KeyStoreSpi::engineStore(LoadStoreParameter) spec misma | haimaychao | Oracle | P3 | security-libs |
| [8217633](../../by-pr/8217/8217633.md) | Configurable extensions with system properties | XueleiFan | Oracle | P3 | security-libs |
| [8023980](../../by-pr/8023/8023980.md) | JCE doesn't provide any class to handle RSA private key | valeriepeng | Oracle | P3 | security-libs |
| [8245194](../../by-pr/8245/8245194.md) | Unix domain socket channel implementation | Michael-Mc-Mahon | Oracle | P4 | core-libs |
| [8244706](../../by-pr/8244/8244706.md) | GZIP "OS" header flag hard-coded to 0 instead of 255 (R | jaikiran | Oracle | P4 | core-libs |
| [8247281](../../by-pr/8247/8247281.md) | migrate ObjectMonitor::_object to OopStorage | dcubed-ojdk | Oracle | P4 | hotspot |

> 共 32 条，仅显示前 20

---

> **统计时间**: 2026-03-25
