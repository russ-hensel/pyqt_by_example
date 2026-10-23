# Showing a self-referencing SQLite table in a QTreeView

Notes carried over from pyqt_by_example. There, `tabs/sql_widgets/tab_q_tree_view_widget.py`
is a working QTreeView demo (4 levels, 41 rows, built from a nested dict).
This file summarizes that tab and the plan for using the same approach on a database table.

## Target situation

- SQLite database.
- One table. Each record has a `parent_id` that points to another record in the
  same table, a one to many relation. This is called an **adjacency list**.
  Root records have `parent_id IS NULL`.
- A few hundred rows.
- **View only**, with no editing or re-parenting.

## What the demo tab does (the parts to reuse)

- **Model.** It uses a `QStandardItemModel`. A "row" is a list of `QStandardItem`s,
  one per column. The children hang off the **first** item of the row, with
  `row[0].appendRow( child_row )`. Top-level rows go on `model.invisibleRootItem()`.
- **Hidden data.** It stores a value on the name item with `item.setData( value, Qt.UserRole )`.
  The tab stores the level number. For the database, store the record `id`.
  Read it back from any clicked column with `index.siblingAtColumn( 0 ).data( Qt.UserRole )`.
- **View setup.**
  - `setModel`
  - `setSelectionBehavior( SelectRows )`
  - `setAlternatingRowColors( True )`
  - `setSortingEnabled( True )`. Call `sortByColumn( 0, Qt.AscendingOrder )` as well,
    or the first sort order looks odd.
  - `setColumnWidth`
- **Expand and collapse.** `expandAll()`, `collapseAll()`, and `expandToDepth( n )`
  (n is 0 based).
- **Signals.** `clicked( QModelIndex )` and `expanded( QModelIndex )`.
- **Path of a node.** Walk `index.parent()` until the index is invalid. This gives
  "Europe / Italy / Rome / Colosseum".
- **Counting.** `rowCount()` counts direct children only. To count every node,
  recurse over `item.child( ix, 0 )`.
- **Finding.** Use `model.findItems( text, Qt.MatchExactly | Qt.MatchRecursive, 0 )`,
  then `setCurrentIndex` and `scrollTo`.
- **Hiding.** `hideColumn( n )` hides a column. `setRowHidden( row, parent_index, True )`
  hides a row, which needs its parent index.
- **Rebuilding.** `model.clear()` also drops the header labels, so set them again.
  Then repopulate.
- **Look.** `header().setSectionResizeMode( ... )`, `setIndentation`,
  `setRootIsDecorated`, `setAnimated`.

## Options considered for the database

1. **Load everything into a `QStandardItemModel` with a two-pass build. This is the
   chosen approach.** One query fetches all rows.
   - Pass 1 makes a row of items per record and keeps a dict `id -> name_item`.
   - Pass 2 attaches each row under `dict[ parent_id ]`, or under the root if
     `parent_id` is NULL.
   - Because of the two passes, the query's row order does not matter.
2. **Recursive CTE.** SQLite's `WITH RECURSIVE` returns rows parent-first, with
   `depth` and path columns. That allows a one-pass build, or subtree queries in SQL.
   This approach does not need it, but it is worth knowing.
3. **Lazy loading.** Query the children of a node when it is expanded, either from the
   `expanded` signal with a dummy child or with `canFetchMore` and `fetchMore`. A fully
   custom `QAbstractItemModel` is another option, where `parent()` is the hard part.
   These are only worth doing for big tables, which this is not.

Qt has no tree-aware SQL model. `QSqlTableModel` and `QSqlQueryModel` are flat.

## Plan for this project (few hundred rows, view only)

Use option 1.

- **Querying.** Use plain `sqlite3`, or `QSqlQuery` if the project already uses
  QtSql. Run `SELECT id, parent_id, name, ... FROM the_table ORDER BY name`.
- **Build pass 1.** For each record, `make_row(...)` creates a list of `QStandardItem`s.
  Store `id` in `Qt.UserRole` on item 0 and call `setEditable( False )` on all of them.
  Keep `items[ id ] = row`.
- **Build pass 2.** For each record, find the parent row, then `parent_row[0].appendRow( row )`.
  If `parent_id` is NULL, append to `invisibleRootItem()`.
- **View only.** Call `tree_view.setEditTriggers( QAbstractItemView.NoEditTriggers )`.
  This is simpler than making every item non-editable.
- **Detail display.** On `clicked`, read the `id` from `UserRole`. Then query or look up
  the full record and show it, for example in a side panel or a message area.

## Things to watch for

- **Orphans.** If `parent_id` points to a missing id, decide what to do.
  Putting the row at the top level and marking it, say with "(orphan)" in a column,
  is easy.
- **Cycles.** A→B→A cannot occur in valid data, but a bad record could create one.
  With the two-pass build, the records in a cycle attach to each other but never
  reach the root, so they silently do not show up.
  - To detect this, compare the recursive count of displayed nodes with the number of
    rows the query returned. A difference means orphans were missed or there is a cycle.
- **Sibling order.** Either `ORDER BY` in the query, since pass 2 appends in that order,
  or turn on view sorting. Do not do both.
- **Several roots** are fine. Each NULL-parent record becomes a top-level row.
- **Refresh.** Call `model.clear()`, then `setHorizontalHeaderLabels(...)`, then rebuild.
  If the expanded state should survive, save the ids of the expanded nodes first and
  re-expand them afterwards.
