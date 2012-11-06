#!/s/sirsi/Unicorn/Bin/perl -w
###########################################################################
# Purpose: Format notices from reports into printable format.
# Method:  TBD.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################
BEGIN # Required for any script that requires the use of epl.pm or other custom modules.
{
	push @INC, "/s/sirsi/Unicorn/EPLwork/epl_perl_libs"; # This is for running 
	push @INC, "/home/ilsdev/projects/epl_perl_libs";    # This is so we can test compile and run on dev machine
}
use strict;
use warnings;
use vars qw/ %opt /;
use Getopt::Std;
use epl;

my $VERSION               = "0.0";
my $HOME_DIR              = qq{.}; # change this for Cron.
# my $HOME_DIR            = qq{/s/sirsi/Unicorn/EPLwork/cronjobscripts/Notices}; # change this for Cron.
my $MIN_ACCT_VALUE        = "10.0";


#
# Message about this program and how to use it
#
sub usage()
{
    print STDERR << "EOF";

	usage: $0 [-b[n]] [-hox]
Formats notice reports into mailable notices.
 -b n : Process Generalized Bill Notices for customers with a floor 
        owed value of 'n' dollars.
 -h   : Process Hold Pickup Notices.
 -o   : Process overdue reminders.
 -x   : This (help) message.

example: $0 -x
example: $0 -b
Version: $VERSION
EOF
    exit;
}

# Kicks off the setting of various switches.
# param:  
# return: 
sub init
{
    my $opt_string = 'b:hox';
    getopts( "$opt_string", \%opt ) or usage();
    usage() if ($opt{'x'});
	$MIN_ACCT_VALUE = scalar( $opt{'n'} ) if ( $opt{'n'} );
}

init();
