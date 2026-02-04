These are the developer notes and scratch pad.

Maybe there is something useful here or not

Table of Contents

---- How these examples are constructed.
---- Work in the pipeline
---- Scratch
---- Versions
---- Tabs from Reading

=================================================

---- Versions
/mnt/WIN_D/russ/0000/python00/python3/_projects/qt5_by_example/tab_select_tab.py

Change list newest at bottom --- really



        fixing custom edits/widget -- just to no exception this round
        these are a bit of a mess

        **   41  42  43 45  46 47  48
        *!
        !!    12   seems to be a mess, custom or not ?? skip for now


        !! bad display on auto select
        !* removed most prints, select still chatty quited it down
        ** report if self.dir_for_tabs is not found
        ** display widgets across top of tab
        ** sort search results
        ** enable close tabs
        !! what to do about rebuild of db
        !! output to a window as well as console  see fitz 23 a or so
        ?? can we do something about dup tabs

        ** add about
        ** add help
        !! add toolbar ??
        !! work on headers and column widths
        ** move select
        ** look for tabs more places
        !! fix for 2 line tabs?
        !! list widget needs lots of work
        *! have version in title and in about
        ** add open parameters

        !! add check that db ( both ) opened and seem ok


    ver_08
        why
            major additions checkpoint
            !! add external ref list
            !! add HOW_COMPLETE

    ver_07
        why
            qt_search tab from other directories
            debug.... and modest additions
            !! salvage old info_about
            ** get rid of old qt_examaple
            !! perhaps work on globals and app services
            !! give a decent icons
            !! add icon to desktop


    ver_06
        why
            qt_search works, time to clean up and consolidate
            debug.... and modest additions

    ver_05
        qt_search.py now works, time to clean up a lot

---- How these examples are constructed.
        Note:
            I am in the middle of a lot of refactoring, these notes are sometime
            a bit insperational, not all of the work is complete yet.

    The "runable" apps here are


       qt_widgets.py


        Individual tabs are now all in ( or being moved into ) their own modules
            like:
                tab_combo_box.py
                .... they all begin with tab_

        utilities that help eveything run are in:

            utils_for_tabs as uft.py
            parameters.y


    the main window for an app, like QtWidgetExamples, QMainWindow and
    its gui is largely base on a QTabWidget.  This widget then
    is used as a container for all the tabs in all the modules.

    You can use the application itself as a tutorial on how a window
    with tabpages might be implemented.


    The wat-inspector applications.

        All the qt examples use the wat-inspector so you can use any one
        of them as a tutorial on how to use the wat-inspector.

        Additionally there are 2 simpler apps that might be a better
        place to start if it is only the wat inspector that interests
        you.

            qt_wat.py
            qt_wat_app.py

    Couple of other modules I am woking into wat-inspector.py:

        info_about.py
        info_about_qt.py

            they do some custom inspection of some classes -- may becoume useful
            in the future.  They are linked to a button that might be called <cust inspect>


    wat_inspector.py is the module with the inspector code it is use by



/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/info_about.py


===============================================================


---- Work in the pipeline

    see general help for each app

        break examples into their own tabs

add this to icons
p.yusukekamiyamane - Free stock icons + pixel fonts
https://p.yusukekamiyamane.com/


wat ideas

        compose into eval from inspection results  -- context menu?
        have ddl as memory to entries


        smooth off edges of gui on what alread have

        pass in a script
        break on exit



    io_qt

        continue migration expansion

qt_exammple ideas

        to many for here, perhaps in helps

When you call self.accept() on a QDialog, it closes the dialog, but it also means that the dialog instance cannot be reused directly to open it again. To open the dialog multiple times, you generally have two options:

    Create a New Instance Each Time: This is the simplest approach. Every time you want to show the dialog, you create a new instance of it.

def open_dialog(self):
    dialog = MyDialog(self)
    if dialog.exec():
        # Process the result if needed
        print("Dialog accepted.")

Use QDialog::hide() Instead of QDialog::accept(): If you want to reuse the same instance of the dialog, call self.hide() instead of self.accept() to close it. Then, you can reopen it by calling self.show() or self.exec() again.

    # Inside the dialog class
    def close_dialog(self):
        self.hide()  # Instead of self.accept()

    # Reopen the dialog
    dialog.show()  # Or dialog.exec() to reopen modally

In many cases, option 1 is simpler and more reliable because it ensures a fresh instance every time. However, if the dialog has a lot of complex setup that you want to preserve, option 2 can work well with minor adjustments.




how to install wat
    conda forge on fattony ok

------------------ xxx ----------------------



SELECT
    people.id,
    people.name,
    people.age,
    people.family_relation,
    people_phones.phone_number
FROM people
LEFT JOIN people_phones ON people.id = people_phones.person_id


I have a QSqlRelationalTableModel that implement the select above.



Some of the code is

        model           = QSqlRelationalTableModel(self)
        self.model      = model
        # self.model          = qt_with_logging.QSqlRelationalTableModelWithLogging(
        #     self )
        model.setTable( "people" )

        debug_var   = self.model.fieldIndex( "id" )   # field name to number

        model.setRelation(
            self.model.fieldIndex( "id" ),  # column name in first table, here people

            QSqlRelation("people_phones", "person_id",      "phone_number")

How can I insert a new record and then update the database.  Can you show the code?




---- Tabs from Reading

    .... Python Rapid Gui Programing.....

            start at 291
            source code at ???


     .... Hands on Qt for Python Developers

            only have sample
           source code at ???

    .... Introdustion to Python Progarming and developing... qt
            look good on basics, but only beginning of qt


    .... uknow.pdf    seems to be Introdustion to Python Progarming and developing... qt
                but including a bit more advanced stuff  not much on sql


    .... Python  GUI Programming   a complete guide

            start 291  compare to    Python Rapid Gui Programing.....



    ....Pythone gui programming a complete Reference Guide       unknown.pdf

        another dup ??

    .... Gui Programming with Python: QT Edition

            Gui Pragramming with Python QT Edition 2002


    Home New Top 20 Popular RSS

Home >> Computers & Internet » Programming » Languages & Tools » Python

Large book cover: GUI Programming with Python: QT Edition

GUI Programming with Python: QT Edition
by Boudewijn Rempt

Publisher: OpenDocs, LLC 2002
ISBN/ASIN: 0970033044
ISBN-13: 9780970033048
Number of pages: 335


    .... Create GUI Applications with Python & Qt5
            The hands-on guide to making apps with Python
            Martin Fitzpatrick
            Version 4.0, 2020-09-12
                    use fitz on the tab key word







---- eof

