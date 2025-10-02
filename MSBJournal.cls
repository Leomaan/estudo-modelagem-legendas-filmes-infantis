% This class file is provided for authors submitting to the
% Modelagem e Simulação de Biossistemas Journal
%
% Version: 1.01 (MODIFIED by Gemini for compatibility), 2025/10/01
%
% Produced by Marcos Figueredo
%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{MSBJournal}[2022/05/10, v1.01]
\AtEndOfClass{\RequirePackage{microtype}}

% Options for element switching
\RequirePackage{xifthen}
\newboolean{displaycopyright}
\newboolean{displaylineno}
\setboolean{displaylineno}{false}

\DeclareOption{lineno}{\setboolean{displaylineno}{true}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{extarticle}}
\ProcessOptions*
\LoadClass{extarticle}

% Line numbers
\RequirePackage[switch,pagewise]{lineno}
\ifthenelse{\boolean{displaylineno}}{\linenumbers}{}

% Fonts and language
\RequirePackage[utf8]{inputenc}

% --- MODIFICAÇÃO PRINCIPAL ---
% O pacote apacite foi removido pois era incompatível com a sua instalação do TeX.
% %\RequirePackage[english,brazil]{apacite}
% O natbib será carregado mais abaixo, de forma correta.
% -----------------------------

\RequirePackage{amsmath,amsfonts,amssymb}
\RequirePackage{mathpazo}
\RequirePackage[scaled]{helvet}
\RequirePackage[T1]{fontenc}
\RequirePackage{url}
\RequirePackage[colorlinks=true, allcolors=blue]{hyperref}
\RequirePackage{lettrine}

% ... (o resto do arquivo permanece o mesmo até a seção de bibliografia) ...

% --- AQUI ESTÁ O RESTANTE DO CÓDIGO SEM ALTERAÇÕES ATÉ A LINHA 106 ---
\newcommand{\watermarkfont}{\color{black50}\normalfont\fontsize{10}{12}\selectfont}
\newcommand{\headerfont}{\normalfont\fontsize{8}{10}\selectfont}
\newcommand{\headerifont}{\normalfont\fontsize{7}{9}\selectfont}
\newcommand{\titlefont}{\color{ppgmsbC3}\normalfont\sffamily\bfseries\fontsize{18}{22}\selectfont}
\newcommand\corresfont{\fontsize{9}{11}\selectfont}
\newcommand{\datesfont}{\normalfont\sffamily\itshape\fontsize{8}{10}\selectfont}
\renewcommand\UrlFont{\color{color1}\sffamily}
\newcommand{\absfont}{\normalfont\sffamily\linespread{1}\fontsize{8.9}{11}\selectfont}
\newcommand{\absheadfont}{\color{ppgmsbC3}\normalfont\sffamily\fontsize{9.4}{11}\selectfont}
\newcommand{\keywordsfont}{\normalfont\sffamily\linespread{1}\fontsize{8.9}{11}\selectfont}
\newcommand{\keywordheadfont}{\normalfont\sffamily\fontsize{7.8}{9}\selectfont\bfseries}
\newcommand{\copyrightfont}{\normalfont\sffamily\fontsize{7}{9}\selectfont}


\RequirePackage{datetime}

\newdateformat{monthyeardate}{%
    \monthname[\THEMONTH] \THEYEAR}

\RequirePackage{enumitem}
\setlist[itemize]{noitemsep}


% Author and affiliation
\RequirePackage{authblk}
\setlength{\affilsep}{9pt}
\renewcommand\Authfont{\color{color0}\fontsize{9.5}{11}\sffamily\selectfont}
\renewcommand\Affilfont{\color{color0}\fontsize{6.5}{9}\selectfont}
\renewcommand\AB@affilsep{\reset@font\protect\Affilfont}
\renewcommand\AB@affilsepx{\reset@font\protect\\\protect\Affilfont}
\renewcommand\Authands{ and }

% Choose article type
\newcommand*{\articletype}[1]{%
    \RequirePackage{#1}}

% Copyright statement
\RequirePackage{textcomp} % For copyright symbol styling
\newcommand{\copyrightstatement}{Copyright \, \textcopyright\, \the\year{} by Programa de Pós-Graduação em Modelagem e Simulação de Biossistemas}

\AtBeginDocument{\setboolean{displaycopyright}{false}}

% Graphics, tables and other formatting
\RequirePackage{graphicx,xcolor}
\RequirePackage{colortbl}
\RequirePackage{booktabs}
\RequirePackage{tikz}
\RequirePackage{algorithm}
\RequirePackage[noend]{algpseudocode}
\RequirePackage{changepage}
\RequirePackage[left=48pt,%
right=42pt,%
top=48pt,%
bottom=60pt,%
headheight=15pt,%
headsep=10pt,%
letterpaper,twoside]{geometry}%
\RequirePackage[labelfont={bf,sf},%
list=no,%
labelsep=space,%
figurename=Figure,%
singlelinecheck=off,%
justification=RaggedRight]{caption}
\setlength{\columnsep}{24pt}
\setlength{\parindent}{12pt}

% Set document color scheme
\definecolor{black50}{gray}{0.5}
\definecolor{color0}{RGB}{0,0,0}
\definecolor{color1}{RGB}{59,90,198}
\definecolor{color3}{RGB}{0,76,113}
\definecolor{ppgmsbC1}{cmyk}{96,0,100,0}
\definecolor{ppgmsbC2}{RGB}{36,96,84}
\definecolor{ppgmsbC3}{RGB}{0,48,58}

% --- SEGUNDA MODIFICAÇÃO PRINCIPAL ---
% A chamada original para natbib foi melhorada para garantir o estilo autor-ano
% e evitar conflitos.
\RequirePackage[round, authoryear]{natbib}
% ------------------------------------

\arrayrulecolor{ppgmsbC2}
\renewcommand{\arraystretch}{1.5}
\captionsetup[table]{position=below}

\newcommand\fs@coloruled{\def\@fs@cfont{\bfseries}\let\@fs@capt\floatc@coloruled
    \def\@fs@pre{\kern2pt}%
    \def\@fs@post{\kern2pt{\color{ppgmsbC3}\hrule}\relax}%
    \def\@fs@mid{\kern2pt{\color{ppgmsbC3}\hrule}\kern2pt}%
    \let\@fs@iftopcapt\iftrue}

\floatstyle{coloruled}
\restylefloat{algorithm}

% ... (o restante do arquivo não precisa de modificações) ...
% O código continua idêntico daqui para baixo.
% Headers and footers
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\pagestyle{fancy}

\newif\ifslugprint\global\slugprintfalse

\def\ouplogo{{\fboxsep0pt\fcolorbox{\typeColorLogo}{\typeColorLogo}{\textcolor{white}{\vbox to 62pt{\vfil\hbox to 85pt{\hfil\fontsize{16}{16}\selectfont \articletypename \hfil}\vspace*{10pt}}}}}\hspace*{12pt}}

\def\slugnote{\global\slugprinttrue}

\def\slugline{\vbox to 0pt{\vspace*{9.5pt}{\headerfont SBMSB, \the\year, ISSN: XXXX-XXXX \vskip-6pt}%
        \rule{121pt}{2pt}\par%
        {\headerifont\color{ppgmsbC3} DOI: 10.1534/SBMSB.XXX.XXXXXX\vskip1pt}%
        {\headerifont IV SIMPÓSIO BAIANO DE MODELAGEM E SIMUÇAÃO DE BIOSSISTEMAS\par}%
        {\headerfont \rec\\
            \rev \\ \acc}}}

\def\firstpageimage{%
    \begin{picture}(0,0)%
        \put(0,-27){\ouplogo}%
        \put(98,-20){\includegraphics[width=.7in]{logoOnly}}%
\end{picture}}

\fancypagestyle{firststyle}{
    \fancyhead[LO,RE,LE,RO]{}
    \ifslugprint\fancyhead[R]{\slugline}\else\fi%
    \fancyhead[L]{\firstpageimage}
}

% Headers
\fancyhead[LO,RE,LE,RO]{}
\lfoot{}
\cfoot{}
\rfoot{}
\fancyhead[RO]{\@runningauthor\hspace{2em}\thepage}
\fancyhead[LE]{\thepage\hspace{2em}\@runningtitle}
\fancyfoot[LO,RE]{}
\renewcommand{\headrulewidth}{0pt}%
\renewcommand{\footrulewidth}{0pt}%

\setcounter{secnumdepth}{0}
\setcounter{tocdepth}{0}

% Section/subsection/paragraph set-up
\RequirePackage[explicit]{titlesec}
\renewcommand{\thesubsection}{\Alph{subsection}}

\titleformat{\section}
{\large\sffamily\bfseries\color{ppgmsbC3}}
{\thesection.}
{0.5em}
{#1}
[]
\titleformat{name=\section,numberless}
{\large\sffamily\bfseries\color{ppgmsbC3}}
{}
{0em}
{#1}
[]
\titleformat{\subsection}
{\bfseries\fontsize{10}{12}\selectfont}
{\thesubsection.}
{0.5em}
{#1}
[]
\titleformat{\subsubsection}[runin]
{\sffamily\bfseries\itshape}
{\thesubsubsection.}
{0.5em}
{#1}
[]
\titleformat{\paragraph}[runin]
{\sffamily\small\bfseries}
{}
{0em}
{#1}
\titlespacing*{\section}{0pc}{3ex \@plus4pt \@minus3pt}{5pt}
\titlespacing*{\subsection}{0pc}{2.5ex \@plus3pt \@minus2pt}{2pt}
\titlespacing*{\subsubsection}{0pc}{2ex \@plus2.5pt \@minus1.5pt}{2pt}
\titlespacing*{\paragraph}{0pc}{1.5ex \@plus2pt \@minus1pt}{12pt}

% Article meta data additional fields
\newcommand{\runningauthor}[1]{\def\@runningauthor{#1}}
\newcommand{\correspondingauthor}[1]{\runningauthor{#1}}
\newcommand{\keywords}[1]{\def\@keywords{#1}}
\newcommand{\runningtitle}[1]{\def\@runningtitle{#1}}
\newcommand{\keywordname}{{\keywordheadfont Keywords:}}

\newcommand{\marginmark}{
    \begin{textblock}{2}(200,9.5)
        \begin{tikzpicture}
            \fill[color=ppgmsbC3] (0,0) rectangle (1.2,0.25);
        \end{tikzpicture}
    \end{textblock}
}

\def\xabstract{abstract}
\long\def\abstract#1\end#2{\def\two{#2}\ifx\two\xabstract
    \long\gdef\theabstract{\ignorespaces#1}
    \def\go{\end{abstract}}\else
\typeout{^^J^^J PLEASE DO NOT USE ANY \string\begin\space \string\end^^J
    COMMANDS WITHIN ABSTRACT^^J^^J}#1\end{#2}
\gdef\theabstract{\vskip12pt BADLY FORMED ABSTRACT: PLEASE DO
NOT USE {\tt\string\begin...\string\end} COMMANDS WITHIN
THE ABSTRACT\vskip12pt}\let\go\relax\fi
\go}

% Set environment for abstract content and styling
\newcommand{\abscontent}{
\noindent
{%
\parbox{\dimexpr\linewidth}{%
    \ifthenelse{\boolean{displaylineno}}{\internallinenumbers}{}%
    {\absheadfont\bfseries Abstract}\vskip3.5pt \absfont \theabstract
}%
\vskip15.5pt%
\noindent
\parbox{\dimexpr\linewidth-2\fboxsep\relax}{%
    \ifthenelse{\boolean{displaylineno}}{\internallinenumbers}{}%
    {\keywordsfont\keywordname}\hspace*{0.1em} \keywordsfont \@keywords%
}%
}%
}%

% Custom title page
\renewcommand{\@maketitle}{\bgroup\setlength{\parindent}{0pt}
{%
\vskip67pt%
{\raggedright \titlefont \@title\vskip13pt}%
{\raggedright \@author\vskip9.5pt}
\ifx\@corres\undefined\vskip6.5pt\else\@corres\vskip11.5pt\fi%
}\egroup%
{%
\vskip12pt%
\abscontent
}%
\vskip25pt%
}%

% Other packages
\RequirePackage{enumitem}
\RequirePackage{tabularx}
\RequirePackage[flushmargin,ragged]{footmisc}

\newlength{\myFootnoteWidth}%
\newlength{\myFootnoteLabel}%
\setlength{\myFootnoteLabel}{0.5em}
\renewcommand{\@makefntext}[1]{%
\setlength{\myFootnoteWidth}{\columnwidth}%
\addtolength{\myFootnoteWidth}{-\myFootnoteLabel}%
\noindent\makebox[\myFootnoteLabel][r]{\@makefnmark\ }%
\parbox[t]{\myFootnoteWidth}{#1}
}

\newdimen\footrulechange
\footrulechange\columnwidth
\renewcommand{\footnoterule}{%
\kern -3pt
{\color{black50} \hrule width \footrulechange height 0.5pt}
\kern 2.5pt
}

\newcommand{\@authfootnote}[2]{%
\begingroup
\setlength{\myFootnoteLabel}{0em}
\renewcommand\thefootnote{}\footnote{\footnotelayout\copyrightfont\textsuperscript{#1}#2}%
\endgroup%
}

\newcommand\blfootnote[1]{%
\@authfootnote{}{#1}%
}
\newcommand\correspondingauthoraffiliation[2][]{%
\gdef\@corres{\corresfont\textsuperscript{#1}#2}%
}

\def\dates#1{\gdef\@dates{#1}}

\def\rec{\textbf{Recevied:} xx/xx/2022.}
\def\rev{\textbf{Revised:} xx/xx/2022}
\def\acc{\textbf{Accepted:} xx/xx/2022}

\newcommand{\equalcontrib}[1]{\@authfootnote{#1}{These authors contributed equally to this work.}}

\newcommand{\firstpagefootnote}{\footrulechange\textwidth%
\blfootnote{\hsize\textwidth doi: 10.1534/ICMSB.XXX.XXXXXX \\%
\ifx\@dates\undefined\vskip0pt\else\@dates\vskip0pt\fi%
Published by Bahia State University \the\year. 
}}

\newenvironment{tableminipage}[1]{\begin{minipage}{#1}\renewcommand\footnoterule{ \kern -1ex}%
\setlength{\myFootnoteLabel}{0.5em}%
}{\end{minipage}}

\def\firstpagebreak{\break\newpage\noindent}

% Package to enable absolute positioning of figures
\RequirePackage[absolute,overlay]{textpos}
\setlength{\TPHorizModule}{1mm}
\setlength{\TPVertModule}{1mm}
\textblockorigin{0mm}{0mm}