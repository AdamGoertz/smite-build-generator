import dependency_injector.containers as containers #type: ignore
import dependency_injector.providers as providers   #type: ignore
from trackers.item_tracker import ItemTracker
from data_objects.item import Item
from graphs.weighted_graph import WeightedGraph
from trackers.build_tracker import BuildTracker
from creators.build_creator import ItemBuildCreator

class Container(containers.DeclarativeContainer):
    graph_factory = providers.Factory(WeightedGraph)

    item_factory = providers.Factory(Item)
    
    item_tracker_factory = providers.DelegatedFactory(ItemTracker)

    build_tracker_factory = providers.Factory(BuildTracker,
                                              graph=graph_factory(),
                                              tracker_factory=item_tracker_factory)


i1 = Container.item_factory("Item1")
i2 = Container.item_factory("Item2")
i3 = Container.item_factory("Item3")
i4 = Container.item_factory("Item4")
i5 = Container.item_factory("Item5")
i6 = Container.item_factory("Item6")
i7 = Container.item_factory("Item7")
i8 = Container.item_factory("Item8")
i9 = Container.item_factory("Item9")
i10 = Container.item_factory("Item10")

build1 = [i1, i2, i3, i4, i5, i6]
build2 = [i1, i3, i2, i4, i5, i6]
build3 = [i1, i3, i2, i4, i5, i6]

build4 = [i1, i2, i7, i8, i9, i10]
build5 = [i1, i2, i7, i8, i9, i10]

bt = Container.build_tracker_factory()
assert isinstance(bt, BuildTracker)

bt.track(build1)
bt.track(build2)
bt.track(build3)
bt.track(build4)
bt.track(build5)


bc = ItemBuildCreator(bt)
print(bc.get_build())







