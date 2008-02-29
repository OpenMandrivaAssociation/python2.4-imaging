%define name python2.4-imaging
%define version 1.1.6
%define release %mkrel 3

Name:		%{name}
Version: 	%{version}
Release: 	%{release}
Summary:	Python's own image processing library 
License:	MIT style
Group:		Development/Python
URL:		http://www.pythonware.com/products/pil/

Source0:	http://www.pythonware.com/downloads/Imaging-%{version}.tar.bz2 
Source1:	pil-handbook.pdf.bz2
Source2:	linux-python-paint-icon.gif
Requires:	python2.4
Requires:	tkinter2.4
Requires:	libjpeg >= 6b
Requires:	zlib >= 1.1.2
Requires:	libpng >= 1.0.1
BuildRequires:	python2.4-devel
BuildRequires:	tkinter2.4
BuildRequires:	jpeg-devel >= 6b
BuildRequires:	png-devel >= 1.0.1
BuildRequires:	X11-devel
BuildRequires:	freetype2-devel
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	tk
BuildRequires:	tk-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Python Imaging Library version %{version}
   
The Python Imaging Library (PIL) adds image processing capabilities 
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%package devel
Summary:	Header files for python-imaging
Group:		Development/C
Requires:	%{name} = %{version}

%description devel
Header files for the Python Imaging Library version %{version}.

%prep
%setup -q -n Imaging-%{version}
bzcat %SOURCE1 > pil-handbook.pdf

# fix tk version
# perl -p -i -e 's/8.3/8.4/g' Setup.in

# fix distutils problem
# %patch
# Make sure to get the right python library
# perl -pi -e "s,(\\\$\((exec_prefix|prefix|exec_installdir)\)|/usr/X11R6)/lib\b,\1/%{_lib},g" Makefile.pre.in Setup.in

# Nuke references to /usr/local
perl -pi -e "s,(-[IL]/usr/local/(include|lib)),,g" setup.py


%build
python2.4 setup.py build_ext -i

%install
rm -fr %{buildroot}
find . -type f | xargs perl -pi -e 's@/usr/local/bin/python@/usr/bin/python@'

python2.4 setup.py install --root=%{buildroot} --record INSTALLED_FILES
pushd libImaging
mkdir -p  %{buildroot}%{_includedir}/python2.4
install -m 644 ImPlatform.h Imaging.h %{buildroot}%{_includedir}/python2.4
popd

# prevent conflict with normal python-imaging package
for bin in %{buildroot}%{_bindir}/*; do
    mv $bin %{buildroot}%{_bindir}/`basename $bin .py`2.4.py
done
perl -pi -e 's|^%{_bindir}/(\w+)\.py$|%{_bindir}/${1}2.4.py|' INSTALLED_FILES

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr (-,root,root)
%doc pil-handbook.pdf Scripts Images Sane CHANGES* README

%files devel
%defattr (-,root,root)
%{_includedir}/python2.4/Imaging.h
%{_includedir}/python2.4/ImPlatform.h
