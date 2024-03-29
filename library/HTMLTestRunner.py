# coding=utf-8
"""
A TestRunner for use with the Python unit testing framework. It
generates a HTML report to show the result at a glance.
The simplest way to use this is to invoke its main method. E.g.
    import unittest
    import HTMLTestRunner
    ... define your tests ...
    if __name__ == '__main__':
        HTMLTestRunner.main()
For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.
    # output to a file
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='My unit test',
                description='This demonstrates the report output by HTMLTestRunner.'
                )
    # Use an external stylesheet.
    # See the Template_mixin class for more customizable options
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'
    # run the test
    runner.run(my_test_suite)
------------------------------------------------------------------------
Copyright (c) 2004-2007, Wai Yip Tung
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name Wai Yip Tung nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__author__ = "Wai Yip Tung,  Findyou"
__version__ = "0.8.2.2"

# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?

import datetime
import sys
import unittest
from xml.sax import saxutils
import os
_real_stdout = sys.stdout
_real_stderr = sys.stderr
ENVIRONMENT_VARIABLE = 'AVAILABLE_DEVICES_SETTING'

# ----------------------------------------------------------------------
# Template

class Template_mixin(object):
    """
    Define a HTML template for report customerization and generation.
    Overall structure of an HTML report
    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
        0: '通过',
        1: '失败',
        2: '错误',
    }

    DEFAULT_TITLE = '自动化测试报告'
    DEFAULT_DESCRIPTION = ''
    DEFAULT_TESTER = ''

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE  html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="zh" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    %(stylesheet)s
</head>
<body class='%(ReportBackgroundStyle)s'>
<script language="javascript" type="text/javascript">
output_list = Array();
/*level 调整增加只显示通过用例的分类 --Findyou
0:Summary //all hiddenRow
1:Failed  //pt hiddenRow, ft none
2:Pass    //pt none, ft hiddenRow
3:All     //pt none, ft none
*/
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level == 2 || level == 0 ) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level < 2) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
    }
    //加入【详细】切换文字变化 --Findyou
    detail_class=document.getElementsByClassName('detail');
	//console.log(detail_class.length)
	if (level == 3) {
		for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="收起"
		}
	}
	else{
			for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="详细"
		}
	}
}
function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        //ID修改 点 为 下划线 -Findyou
        tid0 = 't' + cid.substr(1) + '_' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        //修改点击无法收起的BUG，加入【详细】切换文字变化 --Findyou
        if (toHide) {
            document.getElementById(tid).className = 'hiddenRow';
            document.getElementById(cid).innerText = "详细"
        }
        else {
            document.getElementById(tid).className = '';
            document.getElementById(cid).innerText = "收起"
        }
    }
}
function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}
</script>
%(heading)s
%(report)s
%(ending)s
</body>
</html>
"""
    # variables: (title, generator, stylesheet, heading, report, ending)

    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 80%; }
table       { font-size: 100%; }
/* -- heading ---------------------------------------------------------------------- */
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}
.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}
/* -- body   ------------------------------------------------------------------------ */
.TestSuitePass   { background-color: #dff0d8; }
.TestSuiteFail   { background-color: #efd7d7; }
/* -- report ------------------------------------------------------------------------ */
#total_row  { font-weight: bold; }
table   { background-color: white }
#.AllPass > td   { background-color: #dff0d8; }
#.NotAllPass > td   { background-color: #d9534f; }
tr.passClass > td  { background-color: #9fdc9f; }
tr.failClass > td  { background-color: #ea7e7b; }
tr.errorClass > td  { background-color: #ea7e7b; }
.passCase   { color: #5cb85c; }
.failCase   { color: #d9534f; font-weight: bold; }
.errorCase  { color: #f0ad4e; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }
</style>
"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """<div class='heading'>
<h1 style="font-family: Microsoft YaHei">%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>
"""  # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s : </strong> %(value)s</p>
"""  # variables: (name, value)

    # ------------------------------------------------------------------------
    # Report
    #
    # 汉化,加美化效果 --Findyou
    REPORT_TMPL = """
<p id='show_detail_line'>
<a class="btn btn-primary" href='javascript:showCase(0)'>概要{ %(passrate)s }</a>
<a class="btn btn-danger" href='javascript:showCase(1)'>失败{ %(total_fail)s }</a>
<a class="btn btn-success" href='javascript:showCase(2)'>通过{ %(Pass)s }</a>
<a class="btn btn-info" href='javascript:showCase(3)'>所有{ %(count)s }</a>
</p>
<table id='result_table' class="table table-condensed table-bordered table-hover">
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row' class="text-center %(HeaderStyle)s" style="font-weight: bold;font-size: 14px;">
    <td>用例集/测试用例</td>
    <td>总计</td>
    <td>通过</td>
    <td>失败</td>
    <td>错误</td>
    <td>详细</td>
</tr>
%(test_list)s
<tr id='total_row' class="text-center active">
    <td>总计</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td>通过率：%(passrate)s</td>
</tr>
</table>
"""  # variables: (test_list, count, Pass, fail, error ,passrate)

    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s'>
    <td>%(desc)s</td>
    <td class="text-center">%(count)s</td>
    <td class="text-center">%(Pass)s</td>
    <td class="text-center">%(fail)s</td>
    <td class="text-center">%(error)s</td>
    <td class="text-center"><a href="javascript:showClassDetail('%(cid)s',%(count)s)" class="detail" id='%(cid)s'>详细</a></td>
</tr>
"""  # variables: (style, desc, count, Pass, fail, error, cid)

    # 失败 的样式，去掉原来JS效果，美化展示效果  -Findyou
    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>
    <!--默认收起错误信息 -Findyou   -->
    <button id='btn_%(tid)s' type="button"  class="btn %(ButtonStyle)s btn-xs collapsed" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse" align='left'>
    <!-- 默认展开错误信息 -Findyou 
    <button id='btn_%(tid)s' type="button"  class="btn %(ButtonStyle)s btn-xs" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse in" align='left'> -->
    <pre>
    %(script)s
    </pre>
    </div>
    </td>
</tr>
"""  # variables: (tid, Class, style, desc, status)

    # 通过 的样式，加标签效果  -Findyou
    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'><span class="label label-success success">%(status)s</span></td>
</tr>
"""  # variables: (tid, Class, style, desc, status)

    REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
"""  # variables: (id, output)

    # ------------------------------------------------------------------------
    # ENDING
    #
    # 增加返回顶部按钮  --Findyou
    ENDING_TMPL = """<div id='ending'>&nbsp;</div>
    <div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
    <a href="#"><span class="glyphicon glyphicon-eject" style = "font-size:30px;" aria-hidden="true">
    </span></a></div>
    """


# -------------------- The end of the Template class -------------------


TestResult = unittest.TestResult


class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1, buffer=True):
        super(_TestResult, self).__init__()
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []
        # 增加一个测试通过率 --Findyou
        self.passrate = float(0)
        self.buffer = buffer
        from io import StringIO
        self.log_output = StringIO()

    def _setupStdout(self):
        if getattr(self, 'buffer', None):
            from library.core.utils.common import FlushingStringIO
            self._stderr_buffer = FlushingStringIO(self._dump_test_stderr)
            self._stdout_buffer = FlushingStringIO(self._dump_test_stdout)
            sys.stdout = self._stdout_buffer
            sys.stderr = self._stderr_buffer

    def _restoreStdout(self):
        super(_TestResult, self)._restoreStdout()
        self.log_output.seek(0)
        self.log_output.truncate()

    def startTest(self, test):
        super(_TestResult, self).startTest(test)
        from library.core.TestLogger import TestLogger
        TestLogger.start_test(test)

    def stopTest(self, test):
        from library.core.TestLogger import TestLogger
        TestLogger.stop_test(test)
        super(_TestResult, self).stopTest(test=test)

    def addSuccess(self, test):
        super(_TestResult, self).addSuccess(test)
        from library.core.TestLogger import TestLogger
        from library.core.utils import common
        TestLogger.test_success(test)
        self.success_count += 1
        output = self.log_output.getvalue()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            _real_stdout.write('PASS  {}\n'.format(common.get_test_id(test)))
            _real_stdout.flush()
        else:
            _real_stdout.write('PASS\n')
            _real_stdout.flush()

    def addError(self, test, err):
        from library.core.TestLogger import TestLogger
        from library.core.utils import common
        TestLogger.test_error(test, err)
        self.error_count += 1
        super(_TestResult, self).addError(test, err)
        _, _exc_str = self.errors[-1]
        output = self.log_output.getvalue()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            _real_stdout.write('ERROR {}\n'.format(common.get_test_id(test)))
            _real_stdout.flush()
        else:
            _real_stdout.write('ERROR')
            _real_stdout.flush()

    def addFailure(self, test, err):
        from library.core.TestLogger import TestLogger
        from library.core.utils import common
        TestLogger.test_fail(test, err)
        self.failure_count += 1
        super(_TestResult, self).addFailure(test, err)
        _, _exc_str = self.failures[-1]
        output = self.log_output.getvalue()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            _real_stdout.write('FAIL  {}\n'.format(common.get_test_id(test)))
            _real_stdout.flush()
        else:
            _real_stdout.write('FAIL')
            _real_stdout.flush()

    def addSkip(self, test, reason):
        from library.core.TestLogger import TestLogger
        TestLogger.test_skip(test, reason)
        super(_TestResult, self).addSkip(test, reason)

    def _dump_test_stderr(self, data):
        self.log_output.write(data)
        from library.core.utils import common
        common.write_lines_to_log_file(data)

    def _dump_test_stdout(self, data):
        self.log_output.write(data)
        from library.core.utils import common
        common.write_lines_to_log_file(data)


class HTMLTestRunner(Template_mixin):
    """
    """

    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None, tester=None):
        self.stream = stream
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description
        if tester is None:
            self.tester = self.DEFAULT_TESTER
        else:
            self.tester = tester

        self.startTime = datetime.datetime.now()
        print(self.startTime)
        ###手机号码和手机型号
        from settings import available_devices,setting
        devices_setting_value = os.environ.get(ENVIRONMENT_VARIABLE)   
        devices_setting_value = getattr(available_devices, devices_setting_value, None)
        self.phoneNum=devices_setting_value['M960BDQN229CH']['CARDS'][0]['CARD_NUMBER']
        self.phoneType=devices_setting_value['M960BDQN229CH']['MODEL']['ReadableName']
        ###app-version
        self.appVersion=setting.get_app_version(devices_setting_value['M960BDQN229CH']['DEFAULT_CAPABILITY']['appPackage'])
        print(self.appVersion)
        ###测试执行批次
        from library.core.utils import CommandLineTool
        self.cli_commands = CommandLineTool.parse_and_store_command_line_params()
        self.testBatch = self.cli_commands.testBatch
        self.module_name=self.cli_commands.module_name
        ###测试用例集、测试用例名称
        self.testSuiteName = ''
        self.testCaseName = ''
    def run(self, test):
        "Run the given test case or test suite."
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.generateReport(test, result)
        print('\nTime Elapsed: %s' % (self.stopTime - self.startTime), file=sys.stderr)
        return result

    def sortResult(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n, t, o, e in result_list:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    # 替换测试结果status为通过率 --Findyou
    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        status.append('共 %s' % (result.success_count + result.failure_count + result.error_count))
        if result.success_count: status.append('通过 %s' % result.success_count)
        if result.failure_count: status.append('失败 %s' % result.failure_count)
        if result.error_count:   status.append('错误 %s' % result.error_count)
        if status:
            status = '，'.join(status)
            try:
                self.passrate = str("%.2f%%" % (float(result.success_count) / float(
                    result.success_count + result.failure_count + result.error_count) * 100))
            except ZeroDivisionError:
                self.passrate = 'N/A'
        else:
            status = 'none'
        return [
            ('测试人员', self.tester),
            ('开始时间', startTime),
            ('合计耗时', duration),
            ('测试结果', status + "，通过率= " + self.passrate),
        ]

    def generateReport(self, test, result):
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(
            title=saxutils.escape(self.title),
            generator=generator,
            stylesheet=stylesheet,
            heading=heading,
            report=report,
            ending=ending,
            ReportBackgroundStyle="TestSuitePass" if not (
                result.failure_count or result.error_count) else "TestSuiteFail"
        )
        self.stream.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    # 增加Tester显示 -Findyou
    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=saxutils.escape(name),
                value=saxutils.escape(value),
            )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title=saxutils.escape(self.title),
            parameters=''.join(a_lines),
            description=saxutils.escape(self.description),
            tester=saxutils.escape(self.tester),
        )
        return heading

    # 生成报告  --Findyou添加注释
    def _generate_report(self, result):
        rows = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            # subtotal for a class
            np = nf = ne = 0
            for n, t, o, e in cls_results:
                if n == 0:
                    np += 1
                elif n == 1:
                    nf += 1
                else:
                    ne += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name
            self.testSuiteName = desc  ##测试用例集
            row = self.REPORT_CLASS_TMPL % dict(
                style=ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                desc=desc,
                count=np + nf + ne,
                Pass=np,
                fail=nf,
                error=ne,
                cid='c%s' % (cid + 1),
            )
            rows.append(row)

            for tid, (n, t, o, e) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e)

        report = self.REPORT_TMPL % dict(
            test_list=''.join(rows),
            count=str(result.success_count + result.failure_count + result.error_count),
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            total_fail=str(result.failure_count + result.error_count),
            error=str(result.error_count),
            passrate=self.passrate,
            HeaderStyle='AllPass' if not (result.error_count or result.failure_count) else 'NotAllPass'
        )
        # 将测试结果插入数据库
        from settings.setting import connect_db
        try:
            conn, cursor = connect_db()
        except Exception as e:
            print("connect db fail")

        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        count = result.success_count + result.failure_count + result.error_count
        sql = """
                INSERT INTO test_result (module_name,test_batch,start_time,duration,count,success_count,failure_count,error_count,passrate,remark )
                VALUES ("%s",%d,"%s","%s",%d,%d,%d,%d,"%s","%s");
                """ % (self.module_name,int(self.testBatch),startTime,duration,count,result.success_count,result.failure_count,result.error_count,self.passrate,str(self
                       .cli_commands))
        print(sql)

        try:
            cursor.execute(sql)
            print("insert test result success")
            conn.commit()
            cursor.close()
            conn.close()
            print("close db success")
        except Exception as e:
            print("insert test result fail")
            print(e)
            cursor.close()
            conn.close()
            print("close db success")

        return report

    def _generate_report_test(self, rows, cid, tid, n, t, o, e):
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        # ID修改点为下划线,支持Bootstrap折叠展开特效 - Findyou
        tid = (n == 0 and 'p' or 'f') + 't%s_%s' % (cid + 1, tid + 1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL
        
        # utf-8 支持中文 - Findyou
        # o and e should be byte string because they are collected from stdout and stderr?
        if isinstance(o, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            # uo = o.decode('latin-1')
            uo = o
        else:
            uo = o
        if isinstance(e, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            # ue = e.decode('latin-1')
            ue = e
        else:
            ue = e

        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id=tid,
            # output=saxutils.escape(uo + ue),
            output=saxutils.escape(uo),
        )

        row = tmpl % dict(
            tid=tid,
            Class=(n == 0 and 'hiddenRow' or 'none'),
            style=n == 2 and 'errorCase' or (n == 1 and 'failCase' or 'passCase'),
            ButtonStyle=n == 2 and 'btn-warning' or (n == 1 and 'btn-danger' or 'btn-success'),
            desc=desc,
            script=script,
            status=self.STATUS[n],
        )
        self.testCaseName = desc
        print(self.testBatch)
        print(self.testSuiteName)
        print(self.testCaseName)  ##测试用例
        print(self.phoneNum)
        print(self.phoneType)
        
        print(self.STATUS[n])###打印用例执行结果
        
        ###打印错误信息
        import re
        a= re.finditer(r'(.*Message:.*)|(.*Error:.*)',script)
        for i in a:
            a = i.groups()        
        try:
            a=str(a[0])+str(a[1])
            runInfo=a.replace('None','')
            print(runInfo)
        except Exception  as e:
            runInfo = 'success'
            print(runInfo)
        ###打印用例执行时间
        time= re.findall(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3})',script)
        ##time= re.findall(r'(\d{2}:\d{2}:\d{2}.\d{3})',script)

        runTime = datetime.datetime.strptime(time[-1],"%Y-%m-%dT%H:%M:%S.%f").timestamp() - datetime.datetime.strptime(time[0],"%Y-%m-%dT%H:%M:%S.%f").timestamp()
        print(runTime)
        ####print version



        from settings.setting import connect_db
        try:
            conn, cursor = connect_db()
        except Exception as e:
            print("connect db fail")
        sql = """
        INSERT INTO Autotest_RCS_Andriod (testBatch,appVersion,testSuiteName,testCaseName,phoneType,phoneNum,runStatu,runTime,runInfo )
        VALUES (%d,"%s","%s","%s","%s",%d,"%s","%s","%s");
        """ % (int(self.testBatch), self.appVersion,self.testSuiteName.replace('"',''), self.testCaseName.replace('"',''), self.phoneType,int(self.phoneNum), self.STATUS[n],runTime,runInfo.replace('"',''))
        print(sql)


        try:
            cursor.execute(sql)
            print("insert data success")
            conn.commit()
            cursor.close()
            conn.close()
            print("close db success")
        except Exception as e:
            print("insert data fail")
            print(e)       
            cursor.close()
            conn.close()
            print("close db success")
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL


##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note: Reuse unittest.TestProgram to launch test. In the future we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.
class TestProgram(unittest.TestProgram):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """

    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate HTMLTestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)


main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)
