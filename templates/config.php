<?php

unset($CFG);
global $CFG;
$CFG = new stdClass();

/** Moodle Site config */
$CFG->dbtype    = '%%dbtype%%';
$CFG->dblibrary = 'native';
$CFG->dbhost    = '%%dbhost%%';
$CFG->dbname    = '%%dbname%%';
$CFG->dbuser    = '%%dbuser%%';
$CFG->dbpass    = '%%dbpass%%';
$CFG->prefix    = '%%dbprefix%%';
$CFG->dboptions = array (
  'dbpersist' => 0,
  'dbsocket' => 0,
  'dbport' => '%%dbport%%'
);

$CFG->wwwroot   = 'http://%%phphost%%/moodle';
$CFG->dataroot  = '%%datadir%%/moodle';
$CFG->admin     = 'admin';

/**
 * PHPUnit configuration.
 */
$CFG->phpunit_dataroot = '%%datadir%%/phpunit';
$CFG->phpunit_prefix = 'p_';

/**
 * Behat configuration.
 */
$CFG->behat_wwwroot = 'http://localhost/moodle';
$CFG->behat_dataroot = '%%datadir%%/behat';
$CFG->behat_prefix = 'b_';

if (!empty('%%shareddir%%')) {
    $CFG->behat_screenshots_path = $CFG->behat_faildump_path = '%%shareddir%%/screenshots';
    define ('BEHAT_FEATURE_TIMING_FILE', '%%shareddir%%/timing');
}

$urls = explode(',', '%%seleniumurls%%');

$CFG->behat_config = array(
    'default' => array(
        'extensions' => array(
            'Behat\MinkExtension\Extension' => array(
                'selenium2' => array(
                    'browser' => 'firefox'
                )
            )
        )
    ),
    'phantomjs' => array(
        'filters' => array(
            'tags' => '~@_switch_window&&~@_file_upload&&~@_alert&&~@_bug_phantomjs&&@javascript'
        ),
       'extensions' => array(
           'Behat\MinkExtension\Extension' => array(
               'selenium2' => array(
                   'browser' => 'phantomjs',
               )
           )
       )
    ),
    'phantomjs-selenium' => array(
        'filters' => array(
            'tags' => '~@_switch_window&&~@_file_upload&&~@_alert&&~@_bug_phantomjs&&@javascript'
        ),
       'extensions' => array(
           'Behat\MinkExtension\Extension' => array(
               'selenium2' => array(
                   'browser' => 'phantomjs',
               )
           )
       )
    ),
    'chrome' => array(
        'extensions' => array(
            'Behat\MinkExtension\Extension' => array(
                'selenium2' => array(
                    'browser' => 'chrome',
                )
           )
        )
    ),
    'firefox' => array(
        'extensions' => array(
            'Behat\MinkExtension\Extension' => array(
                'selenium2' => array(
                    'browser' => 'firefox',
                )
            )
        )
    )
);

// If only one selenium url passed, then set it as default profile url.
if (count($urls) == 1) {
    $CFG->behat_config['default'] =
        array(
            'extensions' => array(
                'Behat\MinkExtension\Extension' => array(
                    'selenium2' => array(
                        'browser' => 'firefox',
                        'wd_host' => 'http://'.$urls[0].'/wd/hub'
                    )
                )
            )
        );
}

$counter = 0;
for ($i = %%fromrun%%; $i < %%totalrun%%; $i++) {
    $CFG->behat_parallel_run[$i] = array ('wd_host' => 'http://'.$urls[$counter].'/wd/hub');
    if (!empty($urls[$counter+1])) {
        $counter++;
    }
}

$CFG->directorypermissions = 0777;

require_once(dirname(__FILE__) . '/lib/setup.php');

// There is no php closing tag in this file,
// it is intentional because it prevents trailing whitespace problems!
