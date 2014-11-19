%define luaver 5.2
%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}
%global commit c5270246408557791c6784db0ed2ee2cf32adee9
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           lua-sql
Version:        2.3.0
Release:        3%{?dist}
Summary:        Database connectivity for the Lua programming language

Group:          Development/Libraries
License:        MIT
URL:            http://www.keplerproject.org/luasql/
Source0:        https://github.com/keplerproject/luasql/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  lua >= %{luaver}, lua-devel >= %{luaver}
BuildRequires:  pkgconfig
BuildRequires:  sqlite-devel >= 3.0
BuildRequires:  mysql-devel
BuildRequires:  postgresql-devel

Requires:       lua-sql-sqlite, lua-sql-mysql, lua-sql-postgresql, lua-sql-doc

%description
LuaSQL is a simple interface from Lua to a DBMS. This package of LuaSQL
supports MySQL, SQLite and PostgreSQL databases. You can execute arbitrary SQL
statements and it allows for retrieving results in a row-by-row cursor fashion.

%package doc
Summary:        Documentation for LuaSQL
Group:          Documentation
Requires:       lua >= %{luaver}
%description doc
LuaSQL is a simple interface from Lua to a DBMS. This package contains the
documentation for LuaSQL.


%package sqlite
Summary:        SQLite database connectivity for the Lua programming language
Group:          Development/Libraries
Requires:       lua >= %{luaver}
%description sqlite
LuaSQL is a simple interface from Lua to a DBMS. This package provides access
to SQLite databases.


%package mysql
Summary:        MySQL database connectivity for the Lua programming language
Group:          Development/Libraries
Requires:       lua >= %{luaver}
%description mysql
LuaSQL is a simple interface from Lua to a DBMS. This package provides access
to MySQL databases.


%package postgresql
Summary:        PostgreSQL database connectivity for the Lua programming language
Group:          Development/Libraries
Requires:       lua >= %{luaver}
%description postgresql
LuaSQL is a simple interface from Lua to a DBMS. This package provides access
to PostgreSQL databases.


%prep
%setup -q -n luasql-%{commit}


%build
make %{?_smp_mflags} PREFIX=%{_prefix} DRIVER_INCS="`pkg-config --cflags sqlite3`" DRIVER_LIBS="`pkg-config --libs sqlite3`" T=sqlite3 DEFS="%{optflags} -fPIC"
make %{?_smp_mflags} PREFIX=%{_prefix} DRIVER_INCS="" DRIVER_LIBS="-lpq" T=postgres DEFS="%{optflags} -fPIC" WARN=
make %{?_smp_mflags} PREFIX=%{_prefix} DRIVER_INCS="-I%{_prefix}/include/mysql" DRIVER_LIBS="-L%{_libdir}/mysql -lmysqlclient" T=mysql DEFS="%{optflags} -fPIC"


%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT%{_prefix} LUA_LIBDIR=$RPM_BUILD_ROOT%{lualibdir} LUA_DIR=$RPM_BUILD_ROOT%{luapkgdir} T=sqlite3
make install PREFIX=$RPM_BUILD_ROOT%{_prefix} LUA_LIBDIR=$RPM_BUILD_ROOT%{lualibdir} LUA_DIR=$RPM_BUILD_ROOT%{luapkgdir} T=postgres
make install PREFIX=$RPM_BUILD_ROOT%{_prefix} LUA_LIBDIR=$RPM_BUILD_ROOT%{lualibdir} LUA_DIR=$RPM_BUILD_ROOT%{luapkgdir} T=mysql


%clean
rm -rf $RPM_BUILD_ROOT


%files
# There are no files in the main package

%files doc
%defattr(-,root,root,-)
%doc README
%doc doc/us/*

%files sqlite
%defattr(-,root,root,-)
%dir %{lualibdir}/luasql
%{lualibdir}/luasql/sqlite3.so

%files mysql
%defattr(-,root,root,-)
%dir %{lualibdir}/luasql
%{lualibdir}/luasql/mysql.so

%files postgresql
%defattr(-,root,root,-)
%dir %{lualibdir}/luasql
%{lualibdir}/luasql/postgres.so


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Tom Callaway <spot@fedoraproject.org> - 2.3.0-1
- update to 2.3.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 2.2.0-2
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Mar 22 2011 Tim Niemueller <tim@niemueller.de> - 2.2.0-1
- Upgrade to latest stable release 2.2.0
- Rebuilt for MySQL 5.5
- Added patch for F-14 and up

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Tim Niemueller <tim@niemueller.de> - 2.1.1-5
- Rebuilt for MySQL 5.1

* Tue Apr 08 2008 Tim Niemueller <tim@niemueller.de> - 2.1.1-4
- Main package is now pure meta package to pull in everything else, README
  moved to doc sub-package.

* Sat Apr 05 2008 Tim Niemueller <tim@niemueller.de> - 2.1.1-3
- Do not use pg_config and mysql_config, they are not good for what you think
  they should be used for, cf. #440673

* Fri Apr 04 2008 Tim Niemueller <tim@niemueller.de> - 2.1.1-2
- Fixed lua-sql-postgres requires
- Own %{lualibdir}/luasql directory in all sub-packages

* Fri Apr 04 2008 Tim Niemueller <tim@niemueller.de> - 2.1.1-1
- Initial package

