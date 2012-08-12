%bcond_with marble_python

Name:		marble
Summary:	A virtual globe and world atlas
Version: 4.9.0
Release: 2
Group:		Graphical desktop/KDE
License:	LGPLv2
URL:		http://edu.kde.org
Source:		ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.xz
BuildRequires:	kdelibs4-devel
BuildRequires:	python-devel
BuildRequires:	python-qt4-devel
BuildRequires:	pkgconfig(libgpsd)
BuildConflicts:	qt4-qmlviewer
Requires:	libkdeedu
Requires:	marble-common

%description
Marble is a Virtual Globe and World Atlas that you can use to learn more
about Earth: You can pan and zoom around and you can look up places and
roads. A mouse click on a place label will provide the respective
Wikipedia article.

%files
%doc LICENSE.txt ChangeLog BUGS USECASES MANIFESTO.txt
%doc %{_kde_docdir}/HTML/en/marble
%{_kde_bindir}/marble
%{_kde_bindir}/marble-touch
%{_kde_bindir}/tilecreator
%{_kde_bindir}/routing-instructions
%{_kde_iconsdir}/*/*/apps/marble.*
%{_kde_applicationsdir}/marble.desktop

#---------------------------------------------

%define marblewidget_major 14
%define libmarblewidget %mklibname marblewidget %{marblewidget_major}

%package -n %{libmarblewidget}
Summary:	Runtime library for marble
Group:		System/Libraries
Obsoletes:	%{mklibname marblewidget 13}

%description -n %{libmarblewidget}
Runtime library for marble

%files -n %{libmarblewidget}
%{_kde_libdir}/libmarblewidget.so.0.%{marblewidget_major}*
%{_kde_libdir}/libmarblewidget.so.%{marblewidget_major}

#---------------------------------------------

%package common
Summary:	A virtual globe and world atlas
Group:		Graphical desktop/KDE
%if %with marble_python
BuildRequires:	python-kde4
Requires:	python
%endif

%description common
Marble is a Virtual Globe and World Atlas that you can use to learn more
about Earth: You can pan and zoom around and you can look up places and
roads. A mouse click on a place label will provide the respective
Wikipedia article.

%files -n marble-common
%{_kde_libdir}/kde4/plasma_runner_marble.so
%{_kde_libdir}/kde4/libmarble_part.*
%{_kde_datadir}/config.kcfg/marble.kcfg
%{_kde_services}/marble_part.desktop
%{_kde_services}/plasma-runner-marble.desktop
%{_kde_libdir}/kde4/plugins/marble
%{_kde_appsdir}/marble
%if %with marble_python
%{py_platsitedir}/PyKDE4/marble.so
%endif

#-----------------------------------------------------------------------------

%package -n plasma-applet-kworldclock
Summary:	plasma kworldclock Applet
Group:		Graphical desktop/KDE
Requires:	kdebase4-runtime
Requires:	marble
Provides:	plasma-applet

%description -n plasma-applet-kworldclock
plasma kworldclock Applet

%files -n plasma-applet-kworldclock
%{_kde_libdir}/kde4/plasma_applet_worldclock.so
%{_kde_services}/plasma-applet-kworldclock.desktop

#---------------------------------------------

%package devel
Summary:	Devel stuff for %{name}
Group:		Development/KDE and Qt
Requires:	kdelibs4-devel
Requires:	%{libmarblewidget} = %{EVRD}
Conflicts:	kdeedu4-devel < 4.6.90

%description devel
Files needed to build applications based on %{name}.

%files devel
%{_kde_libdir}/libmarblewidget.so
%{_includedir}/marble
%{_kde_appsdir}/cmake/modules/FindMarble.cmake

#----------------------------------------------------------------------

%prep
%setup -q

%build
%cmake_kde4 \
	%if %without marble_python
	-DEXPERIMENTAL_PYTHON_BINDINGS=FALSE \
	-DBUILD_python=FALSE
	%else
	-DEXPERIMENTAL_PYTHON_BINDINGS=TRUE
	%endif

%make

%install
%makeinstall_std -C build
